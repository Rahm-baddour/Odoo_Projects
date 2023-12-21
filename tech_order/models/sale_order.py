from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        if self.env.user.has_group('tech_order.tech_order_mgr'):
            return super(SaleOrder, self).action_confirm()
        raise ValidationError("User does not exist or does not have permission to perform this action")
