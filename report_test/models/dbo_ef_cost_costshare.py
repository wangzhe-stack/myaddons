# -*- coding: utf-8 -*-

from odoo import models, fields


class EfCostCostShare(models.Model):
    _name = "ef.cost.costshare"
    _description = "ef_cost_costshare"

    i_id = fields.Integer("i_id")
    c_year = fields.Integer("cYear")
    c_month = fields.Integer("cMonth")
    c_dept_code = fields.Char("cDeptCode")
    c_cost_item_code = fields.Char("cCostItemCode")
    i_my_money = fields.Float("iMyMoney", digits=(15, 2))
    i_med_money1 = fields.Float("iMedMoney1", digits=(15, 2))
    i_med_money2 = fields.Float("iMedMoney2", digits=(15, 2))
    i_med_money3 = fields.Float("iMedMoney3", digits=(15, 2))
    i_med_money4 = fields.Float("iMedMoney4", digits=(15, 2))
    i_med_money5 = fields.Float("iMedMoney5", digits=(15, 2))
    i_med_money6 = fields.Float("iMedMoney6", digits=(15, 2))
    i_med_money7 = fields.Float("iMedMoney7", digits=(15, 2))
    i_med_money8 = fields.Float("iMedMoney8", digits=(15, 2))
    i_med_money9 = fields.Float("iMedMoney9", digits=(15, 2))

    i_money1 = fields.Float("iMoney1", digits=(15, 2))
    i_money2 = fields.Float("iMoney2", digits=(15, 2))
    i_money3 = fields.Float("iMoney3", digits=(15, 2))
    i_money4 = fields.Float("iMoney4", digits=(15, 2))
    i_money5 = fields.Float("iMoney5", digits=(15, 2))
    i_money6 = fields.Float("iMoney6", digits=(15, 2))
    i_money7 = fields.Float("iMoney7", digits=(15, 2))
    i_money8 = fields.Float("iMoney8", digits=(15, 2))
    i_money9 = fields.Float("iMoney9", digits=(15, 2))
    i_all_money = fields.Float("iAllMoney", digits=(15, 2))
    i_count_money = fields.Float("iCountMoney", digits=(15, 2))
    cmodifier = fields.Char("cmodifier")
    dnmodifytime = fields.Char("dnmodifytime")