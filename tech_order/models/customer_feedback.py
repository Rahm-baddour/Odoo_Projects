from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta


class CustomerFeedback(models.Model):
    _name = "customer.feedback"
    _description = "Customer Feedback"

    name = fields.Char(string='Name', required=True)
    comment = fields.Char('Comment')
    reason = fields.Char('Reason', readonly=True)
    # 0 is for no rate, and for an odoo widget we limit from 1->3
    rate = fields.Selection([('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], string='Rate')
    customer_id = fields.Many2one('res.partner', string="Customer")
    meal_id = fields.Many2one('order.meal', string="Meal", copy=False)
    state = fields.Selection([('new', 'New'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                             default='new', string='State', readonly=True)

    def action_approved(self):
        if self.state == 'new':
            self.state = 'approved'

    def action_rejected(self):
        if self.state == 'new':
            self.state = 'rejected'