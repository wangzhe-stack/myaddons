# -*- coding: utf-8 -*-
from odoo import _
from odoo import models, fields, api
from odoo.exceptions import ValidationError

from .connect_mssql import MSSQL


class InventoryApply(models.Model):
    _name = 'inventory.apply'
    _description = '物品申领单'
    _rec_name = "apply_no"

    apply_no = fields.Char(string=u'单据号')
    department_id = fields.Many2one('department', string=u'申请部门')
    person_id = fields.Many2one('person', string=u'业务员')
    apply_date = fields.Date(string=u'申领日期', default=fields.Date.today)
    approval_date = fields.Date(string=u'审核日期')
    approval_user = fields.Many2one('person', string=u'审核人')
    approval_memo = fields.Text(string=u'审核意见')
    rd_style = fields.Many2one('rd.style', string=u'出库类别')
    memo = fields.Text(string=u'备注')
    state = fields.Selection([('draft', u"草稿"), ('commit', u'提交审批'), ('approved', u"审批通过"),('unapproved', u"审批不通过")], string="状态",
                             default='draft')

    apply_lines_ids = fields.One2many("inventory.apply.lines", "apply_id", string=u"物品申领明细")

    @api.model
    def create(self, vals):
        if not vals.get('apply_no') or vals['apply_no'] == _('New'):
            vals['apply_no'] = self.env['ir.sequence'].next_by_code('inventory.apply.unique.apply_no') or _('New')
        return super(InventoryApply, self).create(vals)

    @api.onchange('person_id')
    def onchange_person_id(self):
        if self.person_id:
            self.department_id = self.person_id.department_id
            return {'domain': {
                'department_id': [('id', '=', False)],
            }}
        else:
            self.department_id = None
            return {'domain': {
                'department_id': [(1, '=', 1)],
            }}

    @api.onchange('department_id')
    def onchange_department_id(self):
        if self.person_id.department_id != self.department_id:
            self.person_id = None
        if self.department_id:
            return {'domain': {
                'person_id': [('department_id', '=',  self.department_id.id)],
            }}
        else:
            return {'domain': {
                'person_id': [(1, '=', 1)],
                'department_id': [(1, '=', 1)],
            }}

    def button_to_commit(self):
        for record in self:
            record.state = 'commit'

    def button_to_approved(self):
        return {
            'name': _(u'审批窗口'),
            'res_model': self._name,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref("inventory_apply.view_inventory_approve").id,
            'res_id': self.id,
            'target': 'new',
        }

    def oe_save(self):
        self.ensure_one()
        if self.state == 'commit':
            self.state = 'approved'
            # self.approval_user = self.env.user

            ms = MSSQL(host="192.168.0.28:1433", user="sa", pwd="1", db="UFDATA_001_2020")
            rdrecord = ms.execQuery("""SELECT max(id),max(cCode) from rdrecord11""")

            department_code = self.department_id.code
            person_code = self.person_id.code
            person_name = self.person_id.name
            apply_date = self.apply_date.strftime("%Y-%m-%d %H:%M:%S")
            approval_date = self.approval_date.strftime("%Y-%m-%d %H:%M:%S")
            memo = self.memo
            rd_style = self.rd_style.code or ''

            column = """INSERT INTO [dbo].[rdrecord11] ([id],[bRdFlag],[cVouchType],[cBusType], [cSource], [cWhCode], [dDate], [cCode], [cDepCode], [cPersonCode],[bTransFlag], [dnverifytime], [cMaker]"""
            value = f""") values ({int(rdrecord[0][0]) + 1}, 0, N'11', N'领料',N'库存',N'01', N'{apply_date}', {str(int(rdrecord[0][1]) + 1)},  N'{department_code}', N'{person_code}','0',N'{approval_date}',N'{person_name}'"""
            end = """)"""
            if rd_style:
                column += ', [cRdCode]'
                value += f", {rd_style}"
            if memo:
                column += ', [cMemo]'
                value += f", N'{memo}'"
            sql = column + value + end
            ms.execNonQuery(sql)

            for index, apply_line in enumerate(self.apply_lines_ids):
                rdrecordDtl = ms.execQuery("""SELECT max(AutoID) from rdrecords11""")

                inventory_code = apply_line.inventory_code
                number = apply_line.number
                price = apply_line.price
                sum_money = apply_line.sum

                column = """INSERT INTO [dbo].[rdrecords11] ([AutoID],[ID],[cInvCode],[iQuantity],[irowno]"""
                value = f""") values ({int(rdrecordDtl[0][0]) + 1},{int(rdrecord[0][0]) + 1}, N'{inventory_code}',{number},{index+1}"""
                end = """)"""
                if price and sum_money: # 单价，金额
                    column += ', [iUnitCost], [iPrice]'
                    value += f", {price}, {sum_money}"
                dtlSql = column + value + end
                ms.execNonQuery(dtlSql)

    def oe_cancel(self):
        if not self.approval_memo:
            raise ValidationError('审批不通过，意见不能为空')
        if self.state == 'commit':
            self.state = 'unapproved'
            # self.approval_user = self.env.user

    def button_to_draft(self):
        if self.state == 'commit':
            self.state = 'draft'

    def gen_inventory_apply(self, values):
        if not self.env.user.person_ids:
            raise ValidationError("当前登录用户需要绑定业务员！")
        else:
            params = {
                "person_id": self.env.user.person_ids[0].id,
                "department_id": self.env.user.person_ids[0].department_id.id,
            }
            apply_id = self.create(params)
            apply_lines = []
            for line in values:
                res = {
                    'apply_id': apply_id.id,
                    'inventory_id': line['id'],
                    'number': line['number']
                }
                apply_lines.append(res)
            self.env["inventory.apply.lines"].create(apply_lines)
            return apply_id.id


class InventoryApplyLines(models.Model):
    _name = "inventory.apply.lines"
    _description = "物品申领明细"

    apply_id = fields.Many2one("inventory.apply", string=u"申领单ID")
    inventory_id = fields.Many2one("inventory", string=u"物资ID")
    inventory_code = fields.Char(related="inventory_id.code", string=u"物资编码")
    inventory_name = fields.Char(related="inventory_id.name", string=u"物资名称")
    inventory_std = fields.Char(related="inventory_id.c_inv_std", string=u"规格型号")
    c_com_unit_code = fields.Many2one(related="inventory_id.computation_unit_id", string=u"主计量单位")
    price = fields.Float(string=u"单价")
    sum = fields.Float(string=u"金额")
    number = fields.Float(string=u"数量")
    i_quantity = fields.Float(string=u"库存数量")
    demand_date = fields.Date(string=u"需求日期", default=fields.Date.today)
    warehouse_id = fields.Many2one("ware.house", string=u"仓库ID")
    warehouse_name = fields.Char(related="warehouse_id.name", string=u"仓库名称")

    @api.onchange('inventory_id')
    def onchange_inventory_id(self):
        if self.inventory_id:
            ms = MSSQL(host="192.168.0.28:1433", user="sa", pwd="1", db="UFDATA_001_2020")
            resList = ms.execQuery(f"""SELECT cWhCode,sum(iQuantity) FROM CurrentStock where cInvCode = {self.inventory_id.code} GROUP BY cWhCode""")

            if len(resList) == 1:
                self.i_quantity = float(resList[0][1])
                warehouseCode = resList[0][0]
                warehouse_id = self.env['ware.house'].search([('code', '=', warehouseCode)]).id
                self.warehouse_id = warehouse_id
        else:
            self.i_quantity = None
            self.warehouse_id = None

    @api.onchange('warehouse_id')
    def onchange_warehouse_id(self):
        if self.warehouse_id and self.inventory_id:
            ms = MSSQL(host="192.168.0.28:1433", user="sa", pwd="1", db="UFDATA_001_2020")
            resList = ms.execQuery(f"""SELECT cWhCode,sum(iQuantity) FROM CurrentStock 
                          where cInvCode = {self.inventory_id.code} and cWhCode = {self.warehouse_id.code} GROUP BY cWhCode""")
            self.i_quantity = float(resList[0][1]) if resList else None
        else:
            self.i_quantity = None
