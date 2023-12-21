from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta


class OrderItem(models.Model):
    _name = 'order.item'
    _description = 'Order Item'

    order_id = fields.Many2one('order.order', string="Order", readonly=True, copy=False)
    meal_id = fields.Many2one('order.meal', string="Meal", copy=False)
    quantity = fields.Float('Quantity', default=1)
    price = fields.Float('Price')
    total_price = fields.Float('Total Price', compute="_compute_total_price") # store= True,
    state = fields.Selection(related='order_id.state', string="State", store=True)

    def _check_price_negativity(self):
        if self.price < 0:
            return "Price Must be bigger than zero!"
        return False

    # constraints
    @api.constrains('price', 'quantity')
    def check_price_or_quantity_positivity(self):
        for order_item in self:
            if order_item.price < 0:
                raise ValidationError("Price Must be bigger than zero!")
            if order_item.quantity <= 0:
                raise ValidationError("Quantity Must be bigger than zero!")

    # triggers on view actions only
    @api.onchange('meal_id')
    def set_price(self):
        if self._check_price_negativity():
            raise ValidationError("Price Must be bigger than zero!")
        self.price = self.meal_id.price

    #@api.onchange('price', 'quantity')
    # def set_total_price(self):
    #     if self.check_price_or_quantity_positivity():
    #         raise ValidationError("Price and quantity Must be bigger than zero!")
    #     self.total_price = self.price * self.quantity

    # def _check_quantity_negativity(self):
    #     if self.quantity <= 0:
    #         return "Quantity Must be bigger than zero!"
    #     return False
    @api.depends('price', 'quantity')
    def _compute_total_price(self):
        # computable fields deal with all order items
        for order_item in self:
            order_item.total_price = order_item.price * order_item.quantity