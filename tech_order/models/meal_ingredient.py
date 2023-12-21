from odoo import models, fields


class MealIngredient(models.Model):
    _name = "meal.ingredient"
    _description = "Meal Ingredient"

    name = fields.Char("Name", required=True, translate=True)
    quantity = fields.Float("Quantity")
    product_id = fields.Many2one('product.product', string="Product", domain="[('detailed_type', '=', 'product')]")
    meal_id = fields.Many2one('order.meal', string="Meal")
