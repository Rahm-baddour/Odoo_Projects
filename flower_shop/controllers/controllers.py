# -*- coding: utf-8 -*-
# from odoo import http


# class FlowerShop(http.Controller):
#     @http.route('/flower_shop/flower_shop', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/flower_shop/flower_shop/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('flower_shop.listing', {
#             'root': '/flower_shop/flower_shop',
#             'objects': http.request.env['flower_shop.flower_shop'].search([]),
#         })

#     @http.route('/flower_shop/flower_shop/objects/<model("flower_shop.flower_shop"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('flower_shop.object', {
#             'object': obj
#         })
