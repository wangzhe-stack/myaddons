# -*- coding: utf-8 -*-

from odoo import models, fields


class GeoSystemDept(models.Model):
    _name = "geo.system.dept"
    _description = u"部门管理"
    _rec_name = "name"

    name = fields.Char(string=u"部门名称")
    description = fields.Text(string=u"描述")
    parent_id = fields.Many2one("geo.system.dept", string=u"上级部门")


class GeoSystemUser(models.Model):
    _inherit = "res.users"

    # def _default_groups(self):
    #     default_user_id = self.env['ir.model.data'].xmlid_to_res_id('base.default_user', raise_if_not_found=False)
    #     return self.env['res.users'].browse(default_user_id).sudo().groups_id if default_user_id else []

    dept_id = fields.Many2one("geo.system.dept", string=u"部门名称")
    # groups_id = fields.Many2many('res.groups', 'res_groups_users_rel', 'uid', 'gid', string='Groups',
    #                              default=_default_groups)


class GeoSystemGroups(models.Model):
    _inherit = "res.groups"
    _description = u"角色管理"

    description = fields.Text(string="描述")

