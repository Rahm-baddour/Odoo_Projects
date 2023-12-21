from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class RESPartner(models.Model):
    # _name = "res.partner" # Don't put a name if you want to extend, only in inheritance
    # _description = "Res Partner"
    _inherit = "res.partner"

    customer_rank = fields.Float(string="Rank", readonly=True, copy=False)

    def get_meal_rate(self):
        feedbacks = self.env['customer.feedback'].search([('customer_id', '=', self.id)])
        return feedbacks.mapped('meal_id')