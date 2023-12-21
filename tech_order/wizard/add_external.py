from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta


class ExternalItemWizard(models.TransientModel):
    _name = "external.item.wizard"
    _description = "External Item Wizard"

    _transient_max_count = 3
    _transient_max_hours = 3

    def set_default_item(self):
        # search = select *, [] in search = where ..
        external_items = self.env['external.item'].search([])
        return external_items

    external_items = fields.Many2many('external.item', string="External Item", default=set_default_item)

    def add_items(self):
        # context is an odoo session parameter that has the id of the calling order in "active_id"
        # that lets me add external Items to the order that called add_external_items window
        # browse fetch object from its id, the type of expected fetched object is specified by self.env([object_class])
        order = self.env['order.order'].browse(self.env.context.get('active_id'))
        order.external_items = self.external_items