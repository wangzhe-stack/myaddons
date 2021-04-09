# -*- coding: utf-8 -*-

from odoo import models, fields


class EfCostChargeKindData(models.Model):
    _name = "ef.cost.chargekinddata"
    _description = "ef_cost_chargekinddata"

    i_id = fields.Integer("i_id")
    c_charge_kind_code = fields.Char("cChargeKindCode")
    c_order_dept_code = fields.Char("cOrderDeptCode")
    c_exec_dept_code = fields.Char("cExecDeptCode")
    i_money = fields.Float("iMoney", digits=(18, 2))
    c_army = fields.Char("cArmy")
    c_insure = fields.Char("cInsure")
    cdefine22 = fields.Char("cdefine22")
    cdefine23 = fields.Char("cdefine23")
    cdefine24 = fields.Char("cdefine24")
    cdefine25 = fields.Char("cdefine25")
    cdefine26 = fields.Float("cdefine26")
    cdefine27 = fields.Float("cdefine27")
    cdefine28 = fields.Char("cdefine28")
    cdefine29 = fields.Char("cdefine29")
    cdefine30 = fields.Char("cdefine30")
    cdefine31 = fields.Char("cdefine31")
    cdefine32 = fields.Char("cdefine32")
    cdefine33 = fields.Char("cdefine33")
    cdefine34 = fields.Integer("cdefine34")
    cdefine35 = fields.Integer("cdefine35")
    cdefine36 = fields.Datetime("cdefine36")
    cdefine37 = fields.Datetime("cdefine37")
    dnmodifytime = fields.Char("dnmodifytime")
    cmodifier = fields.Char("cmodifier")