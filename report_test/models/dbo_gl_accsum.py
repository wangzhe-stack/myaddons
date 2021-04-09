# -*- coding: utf-8 -*-

from odoo import models, fields


class GlAccsum(models.Model):
    _name = "gl.accsum"
    _description = "gl_accsum"
    _rec_name = "ccode"

    i_id = fields.Integer(u'i_id')
    ccode = fields.Char(u"ccode")
    cexch_name = fields.Char(u"cexch_name")
    iperiod = fields.Integer(u"iperiod")
    cbegind_c = fields.Char(u"cbegind_c")
    cbegind_c_engl = fields.Char(u"cbegind_c_engl")
    mb = fields.Float(u"mb")
    md = fields.Float(u"md")
    mc = fields.Float(u"mc")
    cendd_c = fields.Char(u"cendd_c")
    cendd_c_engl = fields.Char(u"cendd_c_engl")
    me = fields.Float(u"me")
    mb_f = fields.Float(u"mb_f")
    md_f = fields.Float(u"md_f")
    mc_f = fields.Float(u"mc_f")
    me_f = fields.Float(u"me_f")
    nb_s = fields.Float(u"nb_s")
    nd_s = fields.Float(u"nd_s")
    nc_s = fields.Float(u"nc_s")
    ne_s = fields.Float(u"ne_s")
    iyear = fields.Integer("iyear")
    i_yperiod = fields.Integer(u"iYperiod")
