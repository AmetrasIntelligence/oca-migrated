import time
from contextlib import closing

from odoo.addons.queue_job.jobrunner.channels import PENDING
from odoo.addons.queue_job.jobrunner.runner import (
    ERROR_RECOVERY_DELAY,
    Database,
    QueueJobRunner,
    _async_http_get,
    _logger,
    _odoo_now,
)


def reenqueue_job(self, uuid):
    with closing(self.conn.cursor()) as cr:
        cr.execute(
            "UPDATE queue_job SET state=%s " "WHERE uuid=%s",
            (PENDING, uuid),
        )


def get_parent_job_done(self, uuid):
    with closing(self.conn.cursor()) as cr:
        cr.execute(
            "SELECT parent_uuids FROM queue_job WHERE uuid=%s",
            (uuid,),
        )
        parent_uuids = cr.fetchone()
        if parent_uuids and parent_uuids[0]:
            parent_list = tuple(parent_uuids[0].split(", "))
            cr.execute(
                "SELECT state FROM queue_job WHERE uuid in %s",
                (parent_list,),
            )
            parent_state = cr.fetchall()
            parent_state_list = list(set(parent_state))
            if len(parent_state_list) > 1:
                return False
            else:
                if len(parent_state_list) == 1 and parent_state_list[0][0] != "done":
                    return False
        return True


def run_jobs(self):
    now = _odoo_now()
    for job in self.channel_manager.get_jobs_to_run(now):
        if self._stop:
            break
        if self.db_by_name[job.db_name].get_parent_job_done(job.uuid):
            _logger.info("asking Odoo to run job %s on db %s", job.uuid, job.db_name)
            self.db_by_name[job.db_name].set_job_enqueued(job.uuid)
            _async_http_get(
                self.scheme,
                self.host,
                self.port,
                self.user,
                self.password,
                job.db_name,
                job.uuid,
            )
        else:
            self.db_by_name[job.db_name].reenqueue_job(job.uuid)


def run(self):
    _logger.info("starting")
    while not self._stop:
        # outer loop does exception recovery
        try:
            _logger.info("initializing database connections")
            # TODO: how to detect new databases or databases
            #       on which queue_job is installed after server start?
            self.initialize_databases()
            _logger.info("database connections ready")
            started_jobs = self.channel_manager.get_started_jobs()
            for job in started_jobs:
                self.db_by_name[job.db_name].reenqueue_job(job.uuid)
                # inner loop does the normal processing
            while not self._stop:
                self.process_notifications()
                self.run_jobs()
                self.wait_notification()
        except KeyboardInterrupt:
            self.stop()
        except InterruptedError:
            # Interrupted system call, i.e. KeyboardInterrupt during select
            self.stop()
        except Exception:
            _logger.exception(
                "exception: sleeping %ds and retrying", ERROR_RECOVERY_DELAY
            )
            self.close_databases()
            time.sleep(ERROR_RECOVERY_DELAY)
    self.close_databases(remove_jobs=False)
    _logger.info("stopped")


QueueJobRunner.run_jobs = run_jobs
QueueJobRunner.run = run
Database.reenqueue_job = reenqueue_job
Database.get_parent_job_done = get_parent_job_done
