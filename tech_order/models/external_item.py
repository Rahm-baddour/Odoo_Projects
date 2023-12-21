from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta

import logging
_logger = logging.getLogger(__name__)


class ExternalItem(models.Model):
    _name = "external.item"
    _description = "External Items"
    _rec_name = "product_id"

    order_id = fields.Many2many('order.order', string="Orders", readonly=True, copy=False)
    product_id = fields.Many2one('product.product', string="Product")