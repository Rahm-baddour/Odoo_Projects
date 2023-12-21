from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta


class OrderTag(models.Model):
    _name = "order.tag"
    _description = "Order Tags"

    name = fields.Char("Name")
    color = fields.Integer("Color")