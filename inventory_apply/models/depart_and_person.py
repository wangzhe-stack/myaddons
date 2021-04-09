from odoo import models, fields, api


class Department(models.Model):
    _name = 'department'
    _description = '部门表'
    _rec_name = 'name'

    name = fields.Char(string=u'部门名称')
    fullname = fields.Char(string=u'部门全称')
    code = fields.Char(string=u'部门编码')
    type = fields.Selection(compute='_compute_type',
                            selection=[('01', '临床服务类'), ('02', '医技科室'),
                                       ('03', '医疗辅助类'), ('04', '行政后勤类')],
                            string=u'部门分类', store=True)

    @api.depends('fullname', 'code')
    def _compute_type(self):
        for record in self:
            countStr = (record.code[0:2]) if record.code else ''
            record.type = countStr


class Person(models.Model):
    _name = 'person'
    _description = '业务员'
    _rec_name = 'name'

    name = fields.Char(string=u'业务员名称')
    code = fields.Char(string=u'业务员编码')
    department_id = fields.Many2one("department", string=u"所在部门", index=True)
    department_code = fields.Char(related='department_id.code', string=u'部门编码')
    phone = fields.Char(string=u'手机')

    user_id = fields.Many2one("res.users", string=u"用户")


class InventoryUser(models.Model):
    _inherit = "res.users"

    person_ids = fields.One2many("person", "user_id", string=u"业务员")
