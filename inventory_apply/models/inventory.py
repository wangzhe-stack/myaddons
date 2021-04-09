# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from .connect_mssql import MSSQL


class Inventory(models.Model):
    _name = "inventory"
    _description = u"存货档案"
    _rec_name = "code"

    code = fields.Char(string=u"存货编码")
    name = fields.Char(string=u"存货名称")
    c_inv_add_code = fields.Char(string=u"存货代码")
    c_inv_std = fields.Char(string=u"规格型号")
    c_dep_warehouse = fields.Char(string=u"仓库编码")
    warehouse = fields.Char(string=u"仓库", compute="_compute_warehouse", store=True)
    c_position = fields.Char(string=u"货位编码")
    computation_unit_id = fields.Many2one('computation.unit', string=u"主计量单位")
    stock_number = fields.Float(string=u"库存数量", default=0.00, digits=(14, 2))
    image_128 = fields.Image(string=u"图片", max_width=128, max_height=128)
    image_name = fields.Char(string=u"图片名称")

    @api.depends("c_dep_warehouse")
    def _compute_warehouse(self):
        for record in self:
            if record.c_dep_warehouse:
                warehouse = self.env['department'].search([('code', '=', record.c_dep_warehouse)])
                if warehouse:
                    record.warehouse = warehouse.name

    def get_inventory_data(self, ids):
        records = self.search_read([('id', 'in', list(ids))])
        datas = []
        for record in records:
            c_inv_std = record.get('c_inv_std')
            param = {
                'id': record.get('id'),
                'code': record.get('code'),
                'name': record.get('name'),
                'c_inv_std': c_inv_std or '—',
                'computation_unit_name': record.get('computation_unit_id')[1],
                'i_quantity': record.get('stock_number'),
            }
            datas.append(param)
        return datas
