from odoo import models, fields
from collections import defaultdict

class Flower_Product(models.Model):

    _inherit = 'product.product'
    #we extended the produt model to have an is_flower field
    is_flower = fields.Boolean("Is Flower Product?")
    #each flower can have many products associated with it
    flower_id = fields.Many2one("flower.shop.flower")
    sequence_id = fields.Many2one("ir.sequence", "Flower Sequence")
    user_ids = fields.Many2many('res.users')
    needs_watering = fields.Boolean()


    def action_needs_watering(self):

        flowers = self.env["product.product"].search([("is_flower", "=", True)])

        serials = self.env["stock.lot"].search([("product_id", "in", flowers.ids)])

        lot_vals = defaultdict(bool)

        for serial in serials:
            print(serial)

            print('serial.water_ids',serial.water_ids)
            if serial.water_ids:
                last_watered_date = serial.water_ids[0].create_date.date()
                print('last_watered_date',last_watered_date)
                frequency = serial.product_id.flower_id.watering_frequency
                print('frequency',frequency)
                today = fields.Date.today()
                needs_watering = (today - last_watered_date).days >= frequency
                print('needs_watering',needs_watering)
                lot_vals[serial.product_id.id] |= needs_watering
            else:
                lot_vals[serial.product_id.id] = True
        for flower in flowers:
            flower.needs_watering = lot_vals[flower.id]
            print('flower.needs_watering = lot_vals[flower.id]',lot_vals[flower.id])

