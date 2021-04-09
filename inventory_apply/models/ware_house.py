# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WareHouse(models.Model):
    _name = "ware.house"
    _description = u"仓库档案"
    _rec_name = "name"

    code = fields.Char(string=u"仓库编码")
    name = fields.Char(string=u"仓库名称")
    c_dep_code = fields.Char(string=u"所属部门")
    c_wh_address = fields.Char(string=u"仓库地址")
    c_wh_phone = fields.Char(string=u"电话")
    c_wh_person = fields.Char(string=u"负责人")
