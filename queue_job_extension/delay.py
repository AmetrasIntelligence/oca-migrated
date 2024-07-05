from odoo.addons.queue_job.delay import Delayable, DelayableGraph, DelayableRecordset

from .job import JobInherit


class DelayableInherit(Delayable):
    _properties = (
        "priority",
        "eta",
        "max_retries",
        "description",
        "channel",
        "identity_key",
        "parent_uuids",
    )

    def __init__(
        self,
        recordset,
        priority=None,
        eta=None,
        max_retries=None,
        description=None,
        channel=None,
        identity_key=None,
        parent_uuids=None,
    ):
        self._graph = DelayableGraph()
        self._graph.add_vertex(self)

        self.recordset = recordset

        self.priority = priority
        self.eta = eta
        self.max_retries = max_retries
        self.description = description
        self.channel = channel
        self.identity_key = identity_key

        self._job_method = None
        self._job_args = ()
        self._job_kwargs = {}

        self._generated_job = None
        uuid_list = parent_uuids
        if uuid_list:
            uuid_str = ", ".join(uuid_list)
        else:
            uuid_str = ""
        self.parent_uuids = uuid_str

    def _build_job(self):
        if self._generated_job:
            return self._generated_job
        self._generated_job = JobInherit(
            self._job_method,
            args=self._job_args,
            kwargs=self._job_kwargs,
            priority=self.priority,
            max_retries=self.max_retries,
            eta=self.eta,
            description=self.description,
            channel=self.channel,
            identity_key=self.identity_key,
            parent_uuids=self.parent_uuids,
        )
        return self._generated_job


class DelayableRecordsetInherit(DelayableRecordset):
    __slots__ = ("delayable",)

    def __init__(
        self,
        recordset,
        priority=None,
        eta=None,
        max_retries=None,
        description=None,
        channel=None,
        identity_key=None,
        parent_uuids=None,
    ):
        self.delayable = DelayableInherit(
            recordset,
            priority=priority,
            eta=eta,
            max_retries=max_retries,
            description=description,
            channel=channel,
            identity_key=identity_key,
            parent_uuids=parent_uuids,
        )
