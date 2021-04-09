# -*- coding: utf-8 -*-

from odoo import models, fields


class GeoRegulationsLaws(models.Model):
    _name = "geo.regulations.laws"
    _description = "法律法规"
    _rec_name = "name"

    name = fields.Char(string=u"标题")
    file = fields.Binary(string=u"附件")
    file_name = fields.Char(string=u"附件名称")
    content = fields.Html(string=u"正文")


class GeoRegulationsInforms(models.Model):
    _name = "geo.regulations.informs"
    _description = "通知公告"

    name = fields.Char(string=u"标题")
    file = fields.Binary(string=u"附件")
    file_name = fields.Char(string=u"附件名称")
    content = fields.Html(string=u"正文")
