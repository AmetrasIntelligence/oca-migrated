import weakref
from datetime import datetime
from functools import total_ordering

from odoo.addons.queue_job.job import (
    DEFAULT_MAX_RETRIES,
    DEFAULT_PRIORITY,
    PENDING,
    Job,
    _is_model_method,
    _logger,
)


@total_ordering
class JobInherit(Job):
    @classmethod
    def _load_from_db_record(cls, job_db_record):
        stored = job_db_record

        args = stored.args
        kwargs = stored.kwargs
        method_name = stored.method_name

        recordset = stored.records
        method = getattr(recordset, method_name)

        eta = None
        if stored.eta:
            eta = stored.eta
        parent_uuids = None
        if stored.parent_uuids:
            parent_uuids = stored.parent_uuids

        job_ = cls(
            method,
            args=args,
            kwargs=kwargs,
            priority=stored.priority,
            eta=eta,
            job_uuid=stored.uuid,
            description=stored.name,
            channel=stored.channel,
            identity_key=stored.identity_key,
            parent_uuids=parent_uuids,
        )

        if stored.date_created:
            job_.date_created = stored.date_created

        if stored.date_enqueued:
            job_.date_enqueued = stored.date_enqueued

        if stored.date_started:
            job_.date_started = stored.date_started

        if stored.date_done:
            job_.date_done = stored.date_done

        if stored.date_cancelled:
            job_.date_cancelled = stored.date_cancelled

        job_.state = stored.state
        job_.graph_uuid = stored.graph_uuid if stored.graph_uuid else None
        job_.result = stored.result if stored.result else None
        job_.exc_info = stored.exc_info if stored.exc_info else None
        job_.retry = stored.retry
        job_.max_retries = stored.max_retries
        if stored.company_id:
            job_.company_id = stored.company_id.id
        job_.identity_key = stored.identity_key
        job_.worker_pid = stored.worker_pid

        job_.__depends_on_uuids.update(stored.dependencies.get("depends_on", []))
        job_.__reverse_depends_on_uuids.update(
            stored.dependencies.get("reverse_depends_on", [])
        )
        return job_

    @property
    def depends_on(self):
        if not self._depends_on:
            self._depends_on = Job.load_many(self.env, self.__depends_on_uuids)
        return self._depends_on

    @property
    def reverse_depends_on(self):
        if not self._reverse_depends_on:
            self._reverse_depends_on = Job.load_many(
                self.env, self.__reverse_depends_on_uuids
            )
        return set(self._reverse_depends_on)

    # TODO to deprecate (not called anymore)
    @classmethod
    def enqueue(
        cls,
        func,
        args=None,
        kwargs=None,
        priority=None,
        eta=None,
        max_retries=None,
        description=None,
        channel=None,
        identity_key=None,
        parent_uuids=None,
    ):
        """Create a Job and enqueue it in the queue. Return the job uuid.

        This expects the arguments specific to the job to be already extracted
        from the ones to pass to the job function.

        If the identity key is the same than the one in a pending job,
        no job is created and the existing job is returned

        """
        new_job = cls(
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority,
            eta=eta,
            max_retries=max_retries,
            description=description,
            channel=channel,
            identity_key=identity_key,
            parent_uuids=parent_uuids,
        )
        return new_job._enqueue_job()

    def __init__(
        self,
        func,
        args=None,
        kwargs=None,
        priority=None,
        eta=None,
        job_uuid=None,
        max_retries=None,
        description=None,
        channel=None,
        identity_key=None,
        parent_uuids=None,
    ):
        """Create a Job

        :param func: function to execute
        :type func: function
        :param args: arguments for func
        :type args: tuple
        :param kwargs: keyworkd arguments for func
        :type kwargs: dict
        :param priority: priority of the job,
                         the smaller is the higher priority
        :type priority: int
        :param eta: the job can be executed only after this datetime
                           (or now + timedelta)
        :type eta: datetime or timedelta
        :param job_uuid: UUID of the job
        :param max_retries: maximum number of retries before giving up and set
            the job state to 'failed'. A value of 0 means infinite retries.
        :param description: human description of the job. If None, description
            is computed from the function doc or name
        :param channel: The complete channel name to use to process the job.
        :param identity_key: A hash to uniquely identify a job, or a function
                             that returns this hash (the function takes the job
                             as argument)
        """
        if args is None:
            args = ()
        if isinstance(args, list):
            args = tuple(args)
        assert isinstance(args, tuple), "%s: args are not a tuple" % args
        if kwargs is None:
            kwargs = {}

        assert isinstance(kwargs, dict), "%s: kwargs are not a dict" % kwargs

        if not _is_model_method(func):
            raise TypeError("Job accepts only methods of Models")

        recordset = func.__self__
        env = recordset.env
        self.method_name = func.__name__
        self.recordset = recordset

        self.env = env
        self.job_model = self.env["queue.job"]
        self.job_model_name = "queue.job"

        self.job_config = (
            self.env["queue.job.function"].sudo().job_config(self.job_function_name)
        )

        self.state = PENDING

        self.retry = 0
        if max_retries is None:
            self.max_retries = DEFAULT_MAX_RETRIES
        else:
            self.max_retries = max_retries

        self._uuid = job_uuid
        self.graph_uuid = None

        self.args = args
        self.kwargs = kwargs

        self.__depends_on_uuids = set()
        self.__reverse_depends_on_uuids = set()
        self._depends_on = set()
        self._reverse_depends_on = weakref.WeakSet()

        self.priority = priority
        if self.priority is None:
            self.priority = DEFAULT_PRIORITY

        self.date_created = datetime.now()
        self._description = description

        if isinstance(identity_key, str):
            self._identity_key = identity_key
            self._identity_key_func = None
        else:
            # we'll compute the key on the fly when called
            # from the function
            self._identity_key = None
            self._identity_key_func = identity_key

        self.date_enqueued = None
        self.date_started = None
        self.date_done = None
        self.date_cancelled = None

        self.result = None
        self.exc_name = None
        self.exc_message = None
        self.exc_info = None

        if "company_id" in env.context:
            company_id = env.context["company_id"]
        else:
            company_id = env.company.id
        self.company_id = company_id
        self._eta = None
        self.eta = eta
        self.channel = channel
        self.worker_pid = None
        self.parent_uuids = parent_uuids

    def _store_values(self, create=False):
        vals = {
            "state": self.state,
            "priority": self.priority,
            "retry": self.retry,
            "max_retries": self.max_retries,
            "exc_name": self.exc_name,
            "exc_message": self.exc_message,
            "exc_info": self.exc_info,
            "company_id": self.company_id,
            "result": str(self.result) if self.result else False,
            "date_enqueued": False,
            "date_started": False,
            "date_done": False,
            "exec_time": False,
            "date_cancelled": False,
            "eta": False,
            "identity_key": False,
            "worker_pid": self.worker_pid,
            "graph_uuid": self.graph_uuid,
            "parent_uuids": False,
        }

        if self.date_enqueued:
            vals["date_enqueued"] = self.date_enqueued
        if self.date_started:
            vals["date_started"] = self.date_started
        if self.date_done:
            vals["date_done"] = self.date_done
        if self.exec_time:
            vals["exec_time"] = self.exec_time
        if self.date_cancelled:
            vals["date_cancelled"] = self.date_cancelled
        if self.eta:
            vals["eta"] = self.eta
        if self.identity_key:
            vals["identity_key"] = self.identity_key
        if self.parent_uuids:
            vals["parent_uuids"] = self.parent_uuids

        dependencies = {
            "depends_on": [parent.uuid for parent in self.depends_on],
            "reverse_depends_on": [
                children.uuid for children in self.reverse_depends_on
            ],
        }
        vals["dependencies"] = dependencies

        if create:
            vals.update(
                {
                    "user_id": self.env.uid,
                    "channel": self.channel,
                    # The following values must never be modified after the
                    # creation of the job
                    "uuid": self.uuid,
                    "name": self.description,
                    "func_string": self.func_string,
                    "date_created": self.date_created,
                    "model_name": self.recordset._name,
                    "method_name": self.method_name,
                    "job_function_id": self.job_config.job_function_id,
                    "channel_method_name": self.job_function_name,
                    "records": self.recordset,
                    "args": self.args,
                    "kwargs": self.kwargs,
                }
            )

        vals_from_model = self._store_values_from_model()
        # Sanitize values: make sure you cannot screw core values
        vals_from_model = {k: v for k, v in vals_from_model.items() if k not in vals}
        vals.update(vals_from_model)
        return vals


def DelayableRecordset(*args, **kwargs):
    # prevent circular import
    from .delay import DelayableRecordsetInherit as dr

    _logger.debug(
        "DelayableRecordset moved from the queue_job.job"
        " to the queue_job.delay python module"
    )
    return dr(*args, **kwargs)
