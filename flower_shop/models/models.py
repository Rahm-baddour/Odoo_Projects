# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class flower_shop(models.Model):
#     _name = 'flower_shop.flower_shop'
#     _description = 'flower_shop.flower_shop'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
