# -*- coding: utf-8 -*-
import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GeoBaseUnit(models.Model):
    _name = "geo.base.unit"
    _description = u"地勘单位"
    _rec_name = "name"

    name = fields.Char(string=u"单位名称")
    contact_name = fields.Char(string=u"联系人名称")
    contact_phone = fields.Char(string=u"联系人电话")
    address = fields.Char(string=u"地址")
    email = fields.Char(string=u"邮箱")
    position = fields.Char(string=u"联系人职务")
    parent_id = fields.Many2one('geo.base.unit', string=u'隶属于')
    area_geology_level = fields.Selection([('1', u"甲级"), ('2', u"乙级")], string=u"区域地质调查等级")
    liquid_mineral_level = fields.Selection([('1', u"甲级"), ('2', u"乙级")], string=u"液体矿产勘查等级")
    solid_mineral_level = fields.Selection([('1', u"甲级"), ('2', u"乙级")], string=u"固体矿产勘查等级")
    environment_geology_level = fields.Selection([('1', u"甲级"), ('2', u"乙级")], string=u"环境地质勘查等级")
    physical_geography_level = fields.Selection([('1', u"甲级"), ('2', u"乙级")], string=u"地球物理勘查等级")
    geochemistry_level = fields.Selection([('1', u"甲级"), ('2', u"乙级")], string=u"地球化学勘查等级")
    description = fields.Text(string=u"描述")

    @api.constrains("contact_phone", "email")
    def check_phone_and_email(self):
        phone_regex = '^((\+?86)|(\(\+86\)))?(\-|\s)?(13[0 - 9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$|(^(0\d{2,3})?(\-|\s)?\d{7,8}$)'
        email_regex = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'

        if self.contact_phone and not re.match(phone_regex, self.contact_phone):
            raise ValidationError('电话号码格式不正确！')
        if self.email and not re.match(email_regex, self.email):
            raise ValidationError('邮件格式不正确')


class GeoBaseMineral(models.Model):
    _name = "geo.base.mineral"
    _description = u"矿种管理"
    _rec_name = "name"
    _sql_constraints = [
        ('unique_name', 'unique (name)', u'名称不能重复！')
    ]

    name = fields.Char(string=u"名称")
    description = fields.Text(string=u"描述")
    type = fields.Selection([('metal', u"金属"), ("nonmetal", u"非金属"), ("energy", u"能源")], string=u"矿种栏目")


class GeoBaseProspectingStage(models.Model):
    _name = "geo.base.prospecting.stage"
    _description = u"勘查阶段"
    _rec_name = "name"
    _sql_constraints = [
        ('unique_name', 'unique (name)', u'名称不能重复！')
    ]

    name = fields.Char(string=u"名称")
    description = fields.Text(string=u"描述")


class GeoBaseProjectProperty(models.Model):
    _name = "geo.base.project.property"
    _description = u"项目性质"
    _rec_name = "name"
    _sql_constraints = [
        ('unique_name', 'unique (name)', u'名称不能重复！')
    ]

    name = fields.Char(string=u"名称")
    description = fields.Text(string=u"描述")


class GeoBaseAreaManagement(models.Model):
    _name = "geo.base.area.management"
    _description = u"地区管理"
    _rec_name = "name"
    _sql_constraints = [
        ('unique_name', 'unique (name)', u'名称不能重复！')
    ]

    name = fields.Char(string=u"名称")
    description = fields.Text(string=u"描述")


class GeoBaseProjectChangeType(models.Model):
    _name = "geo.base.project.change.type"
    _description = u"项目变更类型"
    _rec_name = "name"
    _sql_constraints = [
        ('unique_name', 'unique (name)', u'名称不能重复！')
    ]

    name = fields.Char(string=u"名称")
    description = fields.Text(string=u"描述")


class GeoBaseBatchCategory(models.Model):
    _name = "geo.base.batch.category"
    _description = u"批次类别维护"
    _rec_name = "name"
    _sql_constraints = [
        ('unique_name', 'unique (name)', u'名称不能重复！')
    ]

    name = fields.Char(string=u"名称")
    description = fields.Text(string=u"描述")


class GeoBaseWorkloadMaintain(models.Model):
    _name = "geo.base.workload.maintain"
    _description = u"工作量维护"
    _rec_name = "name"
    _sql_constraints = [
        ('unique_name', 'unique (name)', u'名称不能重复！')
    ]

    name = fields.Char(string=u"名称")
    description = fields.Text(string=u"描述")


class GeoBaseBatchMaintain(models.Model):
    _name = "geo.base.batch.maintain"
    _description = u"批次维护"
    _rec_name = "name"
    _sql_constraints = [
        ('unique_name', 'unique (name)', u'名称不能重复！')
    ]

    name = fields.Char(string=u"名称")
    description = fields.Text(string=u"描述")

