from odoo import models, fields
class Flower(models.Model):
    _name = 'flower.shop.flower'
    _description = 'Flower'
    # _rec_name = "common_name"

#     flower table fields
    common_name = fields.Char(string='Common Name', required=True)
    scientific_name = fields.Char(string='Scientific Name', required=True)
    season_start_date = fields.Date(string='Season Start Date')
    season_end_date = fields.Date(string='Season End Date')
    watering_frequency = fields.Integer(string='Watering frequency', default=1,help="Frequency is in number of days")
    watering_amount = fields.Float(string='Watering Amount (ml)', default=0.0)

    def name_get(self):
        return [(flower.id, "{} ({})".format(flower.scientific_name, flower.common_name)) for flower in self]