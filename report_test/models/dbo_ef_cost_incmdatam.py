# -*- coding: utf-8 -*-

from odoo import models, fields


class EfCostIncmDataM(models.Model):
    _name = "ef.cost.incmdatam"
    _description = "ef_cost_incmdatam"

    i_id = fields.Integer("i_id")
    c_code = fields.Char("cCode")
    c_vouch_type = fields.Char("cVouchType")
    d_date = fields.Char("dDate")
    c_year = fields.Char("cYear")
    c_month = fields.Char("cMonth")
    i_money = fields.Float("iMoney", digits=(18, 2))
    c_maker = fields.Char("cMaker")
    c_verifier = fields.Char("cVerifier")
    d_veri_date = fields.Char("dVeriDate")
    dcreatesystime = fields.Char("dcreatesystime")
    dnmodifytime = fields.Char("dnmodifytime")
    cmodifier = fields.Char("cmodifier")
    iverifystate = fields.Integer("iverifystate")
    ireturncount = fields.Integer("ireturncount")
    iswfcontrolled = fields.Integer("iswfcontrolled")
    cdefine1 = fields.Char("cdefine1")
    cdefine2 = fields.Char("cdefine2")
    cdefine3 = fields.Char("cdefine3")
    cdefine4 = fields.Datetime("cdefine4")
    cdefine5 = fields.Integer("cdefine5")
    cdefine6 = fields.Datetime("cdefine6")
    cdefine7 = fields.Float("cdefine7")
    cdefine8 = fields.Char("cdefine8")
    cdefine9 = fields.Char("cdefine9")
    cdefine10 = fields.Char("cdefine10")
    cdefine11 = fields.Char("cdefine11")
    cdefine12 = fields.Char("cdefine12")
    cdefine13 = fields.Char("cdefine13")
    cdefine14 = fields.Char("cdefine14")
    cdefine15 = fields.Integer("cdefine15")
    cdefine16 = fields.Float("cdefine16")
    vt_id = fields.Char("VT_ID")
    ufts = fields.Integer("Ufts")
    b_delete = fields.Char("bDelete")

