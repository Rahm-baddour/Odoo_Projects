from odoo import models, fields


class MealCategory(models.Model):
    _name = 'order.meal.category'
    _description = 'Order Meal Category'

    name = fields.Char("Name")