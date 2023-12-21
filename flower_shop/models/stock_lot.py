from odoo import models, fields,api

class StockProductionLot(models.Model):
    _inherit = "stock.lot"

    water_ids = fields.One2many("flower.shop.water", "serial_id")
    is_flower = fields.Boolean(related='product_id.is_flower')
    needs_watering = fields.Boolean(related='product_id.needs_watering')

    def action_water_flower(self):
        print('action_water_flower')
        for flower in self:
            if flower.product_id.is_flower == True:

                print(f"flower is {flower}")
                if flower.water_ids:
                    last_watered_date = flower.water_ids[0].create_date.date()
                    print(f"flower.product_id.name {flower.product_id.name}")
                    print(f"last_watered_date {last_watered_date}")
                    frequency = flower.product_id.flower_id.watering_frequency
                    today = fields.Date.today()
                    if (today - last_watered_date).days < frequency:
                        print('does not need watering' )
                        continue
                print('creating watering record')
                self.env["flower.shop.water"].create({
                    "serial_id": flower.id,
                    # "needs_watering": False,
                 })
                self.env["product.product"].write({
                     "needs_watering": False,
                })
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product = self.env["product.product"].browse(vals["product_id"])
            if product.sequence_id:
                vals["name"] = product.sequence_id.next_by_id()
        return super().create(vals_list)


    def action_open_watering_times(self):
        print('hello')
        return {
            'name': "Watering Times",
            'type': 'ir.actions.act_window',
            'res_model': 'flower.shop.water',
            'view_mode': 'tree,form',
            'view_type': 'form',
            # 'domain': [('id', 'in', self.water_ids)],
            'context': {
                'default_serial_id': self.water_ids,  # Set the default serial_id when creating a new watering time
            },
        }
        # return {'type': 'ir.actions.act_window',
        #         'name': 'wateringids',
        #         'view_mode': 'tree',
        #         'res_model': 'flower.shop.water',
        #         'target': 'new',
        #         'domain': [('id', 'in', self.water_ids)],
        #         # 'context': {'create': True, 'default_meal_id': self.id}
        #         }


