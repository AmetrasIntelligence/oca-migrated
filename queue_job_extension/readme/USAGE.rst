* Using the Odoo configuration file:

  [options]
  (...)
  workers = 6
  server_wide_modules = web,queue_job,ametras_queue_job_parent_child_relation

  (...)
  [queue_job]
  channels = root:2
