from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta



class Meal(models.Model):
    _name = 'order.meal'
    _description = 'Order Meal'
    #for search and suggestions we specify _rec_name
    _rec_name = "name"

    name = fields.Char("Name")
    price = fields.Float("Price")
    # ondelete values are: cascade, restrict, SET NULL, SET DEFAULT, NO ACTION
    category_id = fields.Many2one('order.meal.category', "Category", ondelete="restrict")
    ingredients = fields.One2many('meal.ingredient', 'meal_id', string="Ingredient")
    feedbacks = fields.One2many('customer.feedback', 'meal_id', string="Feedback")

    def action_view_feedback(self):
        return {'type': 'ir.actions.act_window',
                'name': 'feedback',
                'view_mode': 'tree',
                'res_model': 'customer.feedback',
                'target': 'new',
                'domain': [('id', 'in', self.feedbacks.ids)],
                'context': {'create': True, 'default_meal_id':self.id}
                }

    # @api.model work even if there's no object, no self
    @api.model
    def fetch_order(self):
        # ('expected_date', '<', datetime.now()) to work, the expected_date field needs to be stored
        # orders = self.env['order.order'].search([('state', 'in', ('confirmed', 'in_process')),
        #                                          '|',
        #                                          '&', ('order_type', '=', 'external'), ('expected_date', '<', datetime.now()),
        #                                          '&', ('order_type', '=', 'external'), ('table_number', '=', 0)
        #                                          ]) # ,limit=2 gets 2 results ,order = "id",
        #                                             # #count=True (returns the number of records)
        #                                             # instead we can use search_count()
        #                                             # offset=4 num of records to be ignored

        # returns a domain that can be used in search to get the data wanted
        orders = self.read_group( # domain
                                 [('state', 'in', ('confirmed', 'in_process')),
                                                 '|',
                                                 '&', ('order_type', '=', 'external'),
                                                 ('expected_date', '<', datetime.now()),
                                                 '&', ('order_type', '=', 'external'), ('table_number', '=', 0)],
                                 # read those fields
                                 ['name', 'type', 'customer_id'],
                                 # Group by those fields
                                 ['type', 'customer_id'],
                                 orderby = 'order_date', lazy=False # lazy makes it do the group by on all fields specified
                                )
        orders[0].unlink() # same as action delete but from code
        orders[0].copy(default={'name': orders[0].name + ' /test1'}) # same as action duplicate but from code
        #       default ^ is used to prevent error of readonly fields for ex. for end user
        orders_read = orders.read(['name', 'type', 'customer_id'])
        return orders

    #self.ensureone