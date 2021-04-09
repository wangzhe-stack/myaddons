# -*- coding: utf-8 -*-

from odoo import api, fields, models
import json
import logging
import datetime

_logger = logging.getLogger(__name__)


class Member(models.Model):
    _name = 'member'
    _description = u"成员"
    _rec_name = 'name'

    name = fields.Char(u'name')
    first_name = fields.Char(u"First Name")
    last_name = fields.Char(u"Last Name")
    title = fields.Char(u'Title')
    hire_date = fields.Date(u'HireDate')
    birth_date = fields.Date(u'BirthDate')
    phone = fields.Integer(u'Phone')
    gender = fields.Char(u'Gender')
    department_name = fields.Char(u'DepartmentName')

    employee_key = fields.Integer(u'EmployeeKey')
    parent_employee_key = fields.Integer(u'ParentEmployeeKey')

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            if record.first_name and record.last_name:
                record.name = record.first_name + ' ' + record.last_name

    # @api.model
    # def get_data(self):
    #     sql = "select first_name,last_name,title,hire_date,birth_date,employee_key,parent_employee_key from member"
    #     self.env.cr.execute(sql)
    #     dicts = self.env.cr.dictfetchall()
    #     _logger.info(dicts)
    #     return json.dumps(dicts, cls=DateEncoder)


# json模块不支持对时间对象的序列化，此处做处理
# class DateEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.date):
#             return obj.strftime("%Y-%m-%d")
#         else:
#             return json.JSONEncoder.default(self, obj)
