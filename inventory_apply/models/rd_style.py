# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RdStyle(models.Model):
    _name = 'rd.style'
    _description = '出库类别'

    name = fields.Char(string=u'出库名称')
    code = fields.Char(string=u'出库编码')