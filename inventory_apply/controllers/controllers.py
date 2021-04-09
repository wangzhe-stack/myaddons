# -*- coding: utf-8 -*-
from odoo import http

# class InventoryApply(http.Controller):
#     @http.route('/inventory_apply/inventory_apply/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_apply/inventory_apply/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_apply.listing', {
#             'root': '/inventory_apply/inventory_apply',
#             'objects': http.request.env['inventory_apply.inventory_apply'].search([]),
#         })

#     @http.route('/inventory_apply/inventory_apply/objects/<model("inventory_apply.inventory_apply"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_apply.object', {
#             'object': obj
#         })