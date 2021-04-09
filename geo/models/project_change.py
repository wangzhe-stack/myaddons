# -*- coding: utf-8 -*-

from odoo import _
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProjectChange(models.Model):
    _name = "geo.project.change"
    _description = "项目变更"
    _rec_name = "name"

    project_change_id = fields.Integer(related='id')
    project_id = fields.Many2one('geo.project', string=u'变更項目')
    code = fields.Char(related='project_id.code', string=u"项目编号")
    resource_amount = fields.Char(related='project_id.resource_amount', string=u"资源数量")
    area = fields.Many2one("geo.base.area.management", related='project_id.area', string="项目所在地")
    address = fields.Char(related='project_id.address', String=u'详细地址')
    name = fields.Char(related='project_id.name', String=u'项目名称')
    assume_unit = fields.Many2one("geo.base.unit", related='project_id.assume_unit', String=u'承担单位')
    prospecting_unit = fields.Many2one("geo.base.unit", related='project_id.prospecting_unit', String=u'勘查单位')
    batch = fields.Many2one(related='project_id.batch', String=u'项目批次')
    stage = fields.Many2one("geo.base.prospecting.stage", related='project_id.stage', String=u'勘查阶段')
    mineral = fields.Many2many("geo.base.mineral", related='project_id.mineral', String=u'勘查矿种')
    start_date = fields.Date(related='project_id.start_date', String=u'开始时间')
    end_date = fields.Date(related='project_id.end_date', String=u'结束时间')
    approve_date = fields.Date(related='project_id.approve_date', String=u'设计批复时间')
    prospecting_area = fields.Float(related='project_id.prospecting_area', String=u'勘查面积')
    investment_amount = fields.Float(related='project_id.investment_amount', String=u'投资金额')

    #  以下为需要变更字段
    change_type = fields.Many2one('geo.base.project.change.type', string=u'变更类型')
    change_batch = fields.Many2one("geo.base.batch.maintain", string=u'变更批次')
    amount_change_type = fields.Selection([("add", u"增加"), ("dec", u"减少")], string=u'金额变更类型', default='add')
    change_amount = fields.Float(string=u'变更金额', digits=(14,2))
    apply_date = fields.Date(string=u'申请时间')
    approval_date = fields.Date(string=u'批复时间')
    drawings_count = fields.Integer(string=u'附图数量')
    change_content = fields.Html(string=u'变更内容')

    def change_doc(self):
        return {
            'name': _(u'变更文档'),
            'res_model': 'geo.attachment.manage',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref("geo.geo_attachment_manage_form").id,
            'target': 'current',
            'context': {
                'default_stage': 'change',
                'default_project_id': self.project_id.id,
                'form_view_initial_mode': 'edit',
            },
        }