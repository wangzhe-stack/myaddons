# -*- coding: utf-8 -*-

from odoo import models, fields


class EfCostDept(models.Model):
    _name = "ef.cost.dept"
    _description = "ef_cost_dept"
    _rec_name = "c_dept_name"

    i_id = fields.Integer("i_id")
    c_dept_code = fields.Char("cDeptCode")
    c_dept_name = fields.Char("cDeptName")
    c_parent_code = fields.Char("cParentCode")
    c_end = fields.Char("cEnd")
    c_share_kind_code = fields.Char("cShareKindCode")
    c_dept_kind_code = fields.Char("cDeptKindCode")
    c_share_param_code = fields.Char("cShareParamCode")
    c_virtual = fields.Char("cVirtual")
    cmodifier = fields.Char("cmodifier")
    dnmodifytime = fields.Datetime("dnmodifytime")
    u_fts = fields.Integer("Ufts")
    c_level = fields.Char("clevel")
    toc_dept_code = fields.Char("tocDeptCode")
    toc_parent_code = fields.Char("tocParentCode")
    i_grade = fields.Integer("iGrade")
    cks_stop = fields.Char("cksStop")
    c_join_desease = fields.Char("cJoinDesease")
