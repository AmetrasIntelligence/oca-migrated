from odoo.addons.queue_job.jobrunner.channels import Channel, ChannelManager


def get_started_jobs(self):
    return self._running


def manager_get_started_jobs(self):
    return self._root_channel.get_started_jobs()


Channel.get_started_jobs = get_started_jobs
ChannelManager.get_started_jobs = manager_get_started_jobs
