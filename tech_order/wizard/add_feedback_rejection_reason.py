from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta


class FeedbackRejectionReasonWizard(models.TransientModel):
    _name = "feedback.rejection.reason.wizard"
    _description = "Feedback Rejection Reason Wizard"

    reason = fields.Char("Reason", required=True)

    def add_rejection_reason(self):
        feedback = self.env['customer.feedback'].browse(self.env.context.get('active_id'))
        # feedback.state = 'rejected'
        # feedback.reason = self.reason
        feedback.update({'state': 'rejected', 'reason': self.reason})