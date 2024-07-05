# Copyright 2013-2020 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class QueueJob(models.Model):
    _inherit = "queue.job"

    eta = fields.Datetime(string="Execute only after [time]")
    parent_uuids = fields.Char(string="Execute only after [jobs]")
