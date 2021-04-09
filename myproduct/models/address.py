# -*- coding: utf-8 -*-

from odoo import api, fields, models
import json
import logging
import datetime

_logger = logging.getLogger(__name__)


class Address(models.Model):
    _name = 'address'
    _description = u"地址"
    _rec_name = 'province'

    # name = fields.Char(u"名称", default="")
    province = fields.Char(u"省份")
    city = fields.Char(u"城市")
    county = fields.Char(u"县")
    town = fields.Char(u'镇')
    # address = fields.Char(u'具体地址')

    parent_employee_key = fields.Integer(u'ParentEmployeeKey')


