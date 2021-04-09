# -*- coding: utf-8 -*-

from odoo import api, fields, models
import json


class DemoProduct(models.Model):
    _name = 'demo.product'
    _description = u"产品样例"
    _rec_name = 'name'

    name = fields.Char(u'name')
    first_name = fields.Char(u"First Name")
    last_name = fields.Char(u"Last Name")
    product = fields.Char(u"Product")
    available = fields.Boolean(u"Available")
    ship_date = fields.Datetime(u"Ship Date")
    quantity = fields.Integer(u"Quantity")
    price = fields.Float(u'Price')
    attachment_id = fields.Many2many("ir.attachment", "product_res_att_rel", 'att_id', 'product_id',
                                     string=u'attachment')

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            if record.first_name and record.last_name:
                record.name = record.first_name + ' ' + record.last_name

    # @api.model
    # def get_data(self):
    #     sql = "select * from demo_product"
    #     self.env.cr.execute(sql)
    #     dicts = self.env.cr.dictfetchall()
    #     return dicts
