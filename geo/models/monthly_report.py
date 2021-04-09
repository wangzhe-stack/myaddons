# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GeoMonthlyProspectReport(models.Model):
    _name = "geo.monthly.prospect.report"
    _description = u"整装勘查月报填报"
    _rec_name = "name"

    # 基本信息
    report_date = fields.Date(string=u"填报日期")
    report_period = fields.Selection(
        [("1", u"一月"), ('2', u"二月"), ("3", u"三月"), ('4', u"四月"), ("5", u"五月"), ('6', u"六月"),
         ("7", u"七月"), ('8', u"八月"), ("9", u"九月"), ('10', u"十月"), ("11", u"十一月"), ('12', u"十二月")
         ], string="月报期间")
    quarter = fields.Char(string=u"季度")
    project_id = fields.Many2one("geo.project", string=u"整装勘查区名称", domain=[("property.name", "=", u"整装勘查")])
    name = fields.Char(related="project_id.name", string=u"整装勘查区名称")
    prospect_main = fields.Many2one(related="project_id.prospecting_unit", string=u"勘查主体")
    prospect_level = fields.Selection([("1", u"国家级整装勘查区"), ('2', u"省级整装勘查区")], string="勘查区级别")

    report_line_ids = fields.One2many("geo.monthly.prospect.report.line", "report_id", string="整装勘查月报明细")


class GeoMonthlyProspectReportLine(models.Model):
    _name = "geo.monthly.prospect.report.line"
    _description = u"整装勘查月报明细"

    report_id = fields.Many2one("geo.monthly.prospect.report", string=u"整装勘查月报ID")
    # 矿种信息
    mineral = fields.Many2one("geo.base.mineral", string=u"勘查矿种")
    unit = fields.Selection([('1', u"吨"), ('2', u"万吨"), ('3', u"亿吨")], string=u"计量单位")
    # 当月经费投入
    central_finance = fields.Float(string=u"当月中央财政")
    province_finance = fields.Float(string=u"当月省级财政")
    social_funds = fields.Float(string=u"当月社会资金")
    total_finance = fields.Float(string=u"当月总投入")
    # 估算资源量
    reference_above333 = fields.Char(string=u"333及以上备案")
    estimate_above333 = fields.Char(string=u"333及以上估算")
    estimate333 = fields.Char(string=u"333估算")
    total = fields.Char(string=u"合计")
    # 预期成果
    year2_goal = fields.Char(string=u"2年目标")
    finish_percent2 = fields.Float(string=u"2年目标完成比例")
    year5_goal = fields.Char(string=u"5年目标")
    finish_percent5 = fields.Float(string=u"5年目标完成比例")
    # 备注
    note = fields.Text(string=u"备注")
