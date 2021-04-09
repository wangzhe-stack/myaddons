# -*- coding: utf-8 -*-

from odoo import models, fields


class GeoAttachmentManage(models.Model):
    _name = "geo.attachment.manage"
    _description = "附件管理"
    _rec_name = "project_name"

    project_id = fields.Many2one("geo.project", string=u"项目")
    project_name = fields.Char(related="project_id.name", string=u"项目名称")
    project_code = fields.Char(related="project_id.code", string=u"项目编码")
    property = fields.Many2one(related="project_id.property", string=u"项目性质")
    batch = fields.Many2one(related="project_id.batch", string=u"项目批次", store=True)
    assume_unit = fields.Many2one(related="project_id.assume_unit", string=u"承建单位")
    stage = fields.Selection([("set", u"立项阶段"), ('design', u"设计阶段"), ("implement", u"实施阶段"),
                              ("report", u"报告阶段"), ("finish", u"完成阶段"), ('change', u'项目变更')],
                             string=u"项目阶段")
    catalog_id = fields.Many2one("geo.catalog.manage", string=u"附件栏目")
    catalog_name = fields.Char(related="catalog_id.name", string=u"附件栏目名称")
    attachment_ids = fields.Many2many("ir.attachment", string=u"附件")
    attachment_name = fields.Char(string=u"附件名称")


