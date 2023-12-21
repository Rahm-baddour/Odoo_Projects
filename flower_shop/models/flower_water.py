from odoo import models, fields
class FlowerWater(models.Model):
    _name = 'flower.shop.water'
    _description = 'Flower watering'
    # _rec_name = "common_name"
    _order = "create_date"

    serial_id = fields.Many2one("stock.lot")
    # watering_date = fields.Datetime("")
    # flower_id = fields.Many2one('flower.shop.flower', string='Flower', required=True)
    # last_watering_date = fields.Date(string='Watering Date', required=True)