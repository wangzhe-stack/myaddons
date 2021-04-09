# -*- coding: utf-8 -*-
# from odoo import http


# class ReportTest(http.Controller):
#     @http.route('/report_test/report_test/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_test/report_test/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_test.listing', {
#             'root': '/report_test/report_test',
#             'objects': http.request.env['report_test.report_test'].search([]),
#         })

#     @http.route('/report_test/report_test/objects/<model("report_test.report_test"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_test.object', {
#             'object': obj
#         })
