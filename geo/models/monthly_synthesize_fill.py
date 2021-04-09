# -*- coding: utf-8 -*-

from odoo import models, fields


class GeoMonthlySynthesizeFill(models.Model):
    _name = "geo.monthly.synthesize.fill"
    _description = "综合月报填报"
    _rec_name = "name"

    reporting_date= fields.Date(string=u'填报日期',default=fields.Date.context_today)
    reporting_period = fields.Selection(
        [("1", u"一月"), ('2', u"二月"), ("3", u"三月"), ('4', u"四月"), ("5", u"五月"), ('6', u"六月"),
         ("7", u"七月"), ('8', u"八月"), ("9", u"九月"), ('10', u"十月"), ("11", u"十一月"), ('12', u"十二月")
         ], string="月报期间")
    project_id = fields.Many2one('geo.project', string=u'项目名称')
    name = fields.Char(related="project_id.name", string=u"项目名称")
    prospecting_unit = fields.Many2one("geo.base.unit", related='project_id.prospecting_unit', String=u'勘查单位')
    code = fields.Char(related='project_id.code', string=u"项目编码")
    batch = fields.Many2one(related='project_id.batch', String=u'勘查批次')
    plan_funds = fields.Float(related='project_id.investment_amount', string=u"计划经费")
    this_month_funds = fields.Float(string=u"本月执行经费", required=True, digits=(14, 2))
    design_workload = fields.Text(related='project_id.design_workload', string="设计实物工作量")
    complete_workload = fields.Text(string="完成实物工作量")
    main_task = fields.Text(string="主要任务")
    progress_and_results = fields.Text(string="进展与成果")
    memo = fields.Text(string="备注")

