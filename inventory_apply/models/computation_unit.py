# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ComputationUnit(models.Model):
    _name = 'computation.unit'
    _description = '计量单位'
    _order = 'i_number'

    name = fields.Char(string=u'计量单位名称')
    code = fields.Char(string=u'计量单位编码')
    i_number = fields.Integer(string=u'辅计量单位序号')
