# -*- coding: utf-8 -*-
# from odoo import http


# class TechOrder(http.Controller):
#     @http.route('/tech_order/tech_order', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tech_order/tech_order/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tech_order.listing', {
#             'root': '/tech_order/tech_order',
#             'objects': http.request.env['tech_order.tech_order'].search([]),
#         })

#     @http.route('/tech_order/tech_order/objects/<model("tech_order.tech_order"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tech_order.object', {
#             'object': obj
#         })
