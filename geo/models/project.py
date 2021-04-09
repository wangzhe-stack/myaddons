# -*- coding: utf-8 -*-
import datetime

from odoo import _
from odoo import models, fields, api
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _name = "geo.project"
    _description = "项目"
    _rec_name = "name"
    _sql_constraints = [
        ('project_uniq', 'unique (name,code,batch)', "要创建的项目已存在！")
    ]

    # 立项设计
    name = fields.Char(string=u"项目名称", required=True)
    property = fields.Many2one("geo.base.project.property", string=u"项目性质")
    code = fields.Char(string=u"项目编号", required=True)
    area = fields.Many2one("geo.base.area.management", string="项目所在地")
    address = fields.Char(string=u"详细地址", required=True)
    assume_unit = fields.Many2one("geo.base.unit", string=u"承担单位")
    prospecting_unit = fields.Many2one("geo.base.unit", string=u"勘查单位")
    batch = fields.Many2one("geo.base.batch.maintain", string=u"项目批次")
    batch_category = fields.Many2one("geo.base.batch.category", string=u"批次类别")
    stage = fields.Many2one("geo.base.prospecting.stage", string=u"勘查阶段")
    mineral = fields.Many2many("geo.base.mineral", string=u"勘查矿种")
    start_date = fields.Date(string=u"开始时间")
    end_date = fields.Date(string=u"结束时间")
    approve_date = fields.Date(string=u"设计批复时间")
    prospecting_area = fields.Float(string=u"勘查面积", digits=(14, 2))
    investment_amount = fields.Float(string=u"投资金额", required=True, digits=(14, 2))
    resource_amount = fields.Char(string=u"资源数量")
    survey = fields.Html(string=u"项目概况")
    catalog = fields.Text(string=u"项目目录")

    goal = fields.Text(string=u"目标任务")
    design_workload = fields.Text(string="设计工作量")
    expect_result = fields.Text(string=u"预期成果")
    note = fields.Text(string=u"备注")

    # 转为实施阶段
    field_accept_date = fields.Date(string=u"野外验收时间")

    # 转为报告阶段
    review_date = fields.Date(string=u"报告评审时间")
    concurrent_date = fields.Date(string=u"报告汇交时间")
    manage_survey = fields.Text(string=u"经营概况")
    result_summary = fields.Text(string=u"成果简介")

    # 转为完结
    # 暂时未有需要填写的字段

    status = fields.Selection([("set", u"立项"), ('design', u"设计"), ("implement", u"实施"),
                               ("report", u"报告"), ("finish", "完成")], string=u"项目状态", default="set")
    workload_ids = fields.One2many("geo.project.workload", "project_id", string=u"工作量工作项目明细")
    coordinate_ids = fields.One2many("geo.project.coordinate", "project_id", string=u"拐点坐标")
    attachments = fields.One2many("geo.attachment.manage", "project_id", string=u"附件上传")
    project_changes = fields.One2many("geo.project.change", "project_id", string=u"项目变更")

    # 位置信息
    longitude = fields.Float(string="经度", digits=(9, 6))
    latitude = fields.Float(string="纬度", digits=(9, 6))

    @api.onchange('start_date', 'end_date')
    def check_time(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('开始时间不能大于结束时间！')
        if self.end_date and self.end_date < datetime.date.today():
            raise ValidationError("结束时间不能小于现在！")

    def set_to_design(self):
        self.ensure_one()
        if self.status == 'set':
            self.status = 'design'

    def design_to_implement(self):
        return {
            'name': _(u'转为实施'),
            'res_model': self._name,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref("geo.geo_project_design_to_implement").id,
            'res_id': self.id,
            'target': 'new',
            'context': {
                'form_view_initial_mode': 'edit',
            },
        }

    def implement_to_report(self):
        return {
            'name': _(u'转为报告'),
            'res_model': self._name,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref("geo.geo_project_implement_to_report").id,
            'res_id': self.id,
            'target': 'new',
            'context': {
                'form_view_initial_mode': 'edit',
            },
        }

    def report_to_finish(self):
        self.ensure_one()
        if self.status == 'report':
            self.status = 'finish'

    def upload_doc(self):
        return {
            'name': _(u'附件上传'),
            'res_model': 'geo.attachment.manage',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref("geo.geo_attachment_manage_form").id,
            'target': 'current',
            'context': {
                'default_stage': self.status,
                'default_project_id': self.id,
                'form_view_initial_mode': 'edit',
            },
        }

    def view_doc(self):
        env = self.env.context
        if 'status' in env:
            domain = [('project_id', '=', self.id)]
            if env['status'] == 'set':
                domain.append(('stage', '=', 'set'))
            elif env['status'] == 'design':
                domain.append(('stage', '=', 'design'))
            elif env['status'] == 'implement':
                domain.append(('stage', '=', 'implement'))
            elif env['status'] == 'report':
                domain.append(('stage', '=', 'report'))
            return {
                'type': 'ir.actions.act_window',
                'name': _(u'附件浏览'),
                'res_model': 'geo.attachment.manage',
                'view_mode': 'tree,form',
                'target': 'current',
                'domain': domain,
                'context': dict(create=False,delete=False,edit=False)
            }

    def save(self):
        self.ensure_one()
        if self.status == 'set':
            self.status = 'design'
        elif self.status == 'design':
            self.status = 'implement'
        elif self.status == 'implement':
            self.status = 'report'

    def project_change(self):
        return {
            'name': _(u'项目变更'),
            'res_model': "geo.project.change",
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref("geo.view_geo_project_change_form").id,
            'target': 'current',
            'context': {'default_project_id': self.id},
        }

    def project_doc_view(self):
        if not self.attachments:
            raise ValidationError('该项目没有相关文档。')
        return {
            'name': _(u'项目文档'),
            'res_model': "geo.attachment.manage",
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'domain': [('project_id', '=', self.id)],
            'context': dict(self._context, create=False,delete=False,group_by='catalog_id')
        }

    def project_change_record(self):
        if not self.project_changes:
            raise ValidationError('该项目没有变更记录。')
        return {
            'name': _(u'项目变更记录'),
            'res_model': "geo.project.change",
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            # 'view_id': self.env.ref("geo.view_geo_project_change_tree").id,
            'domain': [('project_id', '=', self.id)],
            'context': dict(self._context, create=False)
        }

    def search_position(self, code, name):
        records = self.search(["|", ("name", "=", name), ("code", "=", code)])
        data = []
        for record in records:
            params = {
                "name": record.name,
                "area": record.area.name,
                "assume_unit": record.assume_unit.name,
                "position": [record.longitude, record.latitude],
            }
            data.append(params)
        _logger.info(data)
        return data


class GeoProjectWorkload(models.Model):
    _name = "geo.project.workload"
    _description = "工作量工作项目明细"

    project_id = fields.Many2one("geo.project", string=u"项目")
    name = fields.Many2one("geo.base.workload.maintain", string=u"工作项目")
    workload = fields.Char(string=u"工作量")


class GeoProjectCoordinate(models.Model):
    _name = "geo.project.coordinate"
    _description = "拐点坐标"

    project_id = fields.Many2one("geo.project", string=u"项目")
    # 拐点坐标
    coordinate54 = fields.Text(string=u"54坐标")
    coordinate80 = fields.Text(string=u"80坐标")
