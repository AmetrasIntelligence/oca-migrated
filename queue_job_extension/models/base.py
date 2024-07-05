from odoo import models

ERROR_RECOVERY_DELAY = 5
from ..delay import DelayableInherit  # noqa: E402
from ..job import DelayableRecordset  # noqa: E402


class Base(models.AbstractModel):
    """The base model, which is implicitly inherited by all models.

    A new :meth:`~with_delay` method is added on all Odoo Models, allowing to
    postpone the execution of a job method in an asynchronous process.
    """

    _inherit = "base"

    def with_delay(
        self,
        priority=None,
        eta=None,
        max_retries=None,
        description=None,
        channel=None,
        identity_key=None,
        parent_uuids=None,
    ):
        """Return a ``DelayableRecordset``

        It is a shortcut for the longer form as shown below::

            self.with_delay(priority=20).action_done()
            # is equivalent to:
            self.delayable().set(priority=20).action_done().delay()

        ``with_delay()`` accepts job properties which specify how the job will
        be executed.

        Usage with job properties::

            env['a.model'].with_delay(priority=30, eta=60*60*5).action_done()
            delayable.export_one_thing(the_thing_to_export)
            # => the job will be executed with a low priority and not before a
            # delay of 5 hours from now

        When using :meth:``with_delay``, the final ``delay()`` is implicit.
        See the documentation of :meth:``delayable`` for more details.

        :param parent_uuids: Do not run job before job parent_uuids is done.
        :return: instance of a DelayableRecordset
        :rtype: :class:`odoo.addons.queue_job.job.DelayableRecordset`
        """
        return DelayableRecordset(
            self,
            priority=priority,
            eta=eta,
            max_retries=max_retries,
            description=description,
            channel=channel,
            identity_key=identity_key,
            parent_uuids=parent_uuids,
        )

    def delayable(
        self,
        priority=None,
        eta=None,
        max_retries=None,
        description=None,
        channel=None,
        identity_key=None,
        parent_uuids=None,
    ):
        """Return a ``Delayable``

        The returned instance allows to enqueue any method of the recordset's
        Model.

        Usage::

            delayable = self.env["res.users"].browse(10).delayable(priority=20)
            delayable.do_work(name="test"}).delay()

        In this example, the ``do_work`` method will not be executed directly.
        It will be executed in an asynchronous job.

        Method calls on a Delayable generally return themselves, so calls can
        be chained together::

            delayable.set(priority=15).do_work(name="test"}).delay()

        The order of the calls that build the job is not relevant, beside
        the call to ``delay()`` that must happen at the very end. This is
        equivalent to the example above::

            delayable.do_work(name="test"}).set(priority=15).delay()

        Very importantly, ``delay()`` must be called on the top-most parent
        of a chain of jobs, so if you have this::

            job1 = record1.delayable().do_work()
            job2 = record2.delayable().do_work()
            job1.on_done(job2)

        The ``delay()`` call must be made on ``job1``, otherwise ``job2`` will
        be delayed, but ``job1`` will never be. When done on ``job1``, the
        ``delay()`` call will traverse the graph of jobs and delay all of
        them::

            job1.delay()

        For more details on the graph dependencies, read the documentation of
        :module:`~odoo.addons.queue_job.delay`.

        :param priority: Priority of the job, 0 being the higher priority.
                            Default is 10.
        :param eta: Estimated Time of Arrival of the job. It will not be
                    executed before this date/time.
        :param max_retries: maximum number of retries before giving up and set
                                the job state to 'failed'. A value of 0 means
                                infinite retries.  Default is 5.
        :param description: human description of the job. If None, description
                                is computed from the function doc or name
        :param channel: the complete name of the channel to use to process
                            the function. If specified it overrides the one
                            defined on the function
        :param identity_key: key uniquely identifying the job, if specified
                                 and a job with the same key has not yet been run,
                                 the new job will not be added. It is either a
                                 string, either a function that takes the job as
                                 argument (see :py:func:`..job.identity_exact`).
                                 the new job will not be added.
        :return: instance of a Delayable
        :rtype: :class:`odoo.addons.queue_job.job.Delayable`
        """
        return DelayableInherit(
            self,
            priority=priority,
            eta=eta,
            max_retries=max_retries,
            description=description,
            channel=channel,
            identity_key=identity_key,
            parent_uuids=parent_uuids,
        )
