# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import logging

from odoo.osv import expression

_logger = logging.getLogger(__name__)


class GeoParamSetting(models.Model):
    _name = "geo.param.setting"
    _description = u"参数设置"
    _rec_name = "name"

    name = fields.Char(string=u"名称")
    description = fields.Text(string=u"概述")


class GeoDocCatalog(models.Model):
    _name = "geo.doc.catalog"
    _description = u"文档目录"
    _rec_name = "name"

    name = fields.Char(string=u"名称")
    parent_id = fields.Many2one("geo.doc.log", string=u"父节点")
    description = fields.Text(string=u"概述")


class GeoCatalogManage(models.Model):
    _name = "geo.catalog.manage"
    _description = u"目录管理"
    _rec_name = "full_name"

    name = fields.Char(string=u"名称")
    parent_id = fields.Many2one("geo.catalog.manage", string=u"父节点", index=True)
    child_ids = fields.One2many("geo.catalog.manage", 'parent_id', string=u"子节点")
    description = fields.Text(string="描述")
    full_name = fields.Char(compute="_compute_full_name", string=u"目录全称", store=True)

    @api.depends('name', 'parent_id.full_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = rec._get_full_name()

    def _get_full_name(self, level=6):
        """ Return the full name of ``self`` (up to a certain level). """
        if level <= 0:
            return '...'
        if self.parent_id:
            return self.parent_id._get_full_name(level - 1) + '/' + (self.name or "")
        else:
            return self.name

    @api.constrains("parent_id")
    def _check_parent(self):
        if self.parent_id == self.id:
            raise ValidationError("请勿选择本身作为父节点！")

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        # 按照附件的 项目阶段 字段，过滤 该项目阶段下的附件栏目
        stage = self._context.get('stage', None)
        if stage:
            value = dict(self.env['geo.attachment.manage'].fields_get(allfields=['stage'])['stage']['selection']).get(
                stage)
            domain = ['&', ('full_name', 'like', value), ('child_ids', '=', False)]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super()._name_search(name=name, args=args, operator=operator, limit=limit,
                                    name_get_uid=name_get_uid)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # 按照附件的 项目阶段 字段，过滤 该项目阶段下的附件栏目
        stage = self._context.get('stage', None)
        if stage:
            value = dict(self.env['geo.attachment.manage'].fields_get(allfields=['stage'])['stage']['selection']).get(
                stage)
            newDomain = ['&', ('full_name', 'like', value), ('child_ids', '=', False)]
            return super().search_read(expression.AND([domain, newDomain]), fields, offset, limit, order)

        return super().search_read(domain, fields, offset, limit, order)
