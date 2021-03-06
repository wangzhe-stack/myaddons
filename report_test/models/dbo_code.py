# -*- coding: utf-8 -*-

from odoo import models, fields


class Code(models.Model):
    _name = 'code'
    _description = u"Code"
    _rec_name = 'ccode'

    i_id = fields.Integer(u'i_id')
    cclass = fields.Char(u'cclass')
    cclass_engl = fields.Char(u"cclass_engl")
    cclassany = fields.Char(u"cclassany")
    cclassany_engl = fields.Char(u'cclassany_engl')
    ccode = fields.Char(u'ccode')
    ccode_name = fields.Char(u'ccode_name')
    ccode_engl = fields.Char(u'ccode_engl')
    igrade = fields.Integer(u'igrade')
    bproperty = fields.Boolean(u'bproperty')
    cbook_type = fields.Char(u'cbook_type')
    cbook_type_engl = fields.Char(u'cbook_type_engl')
    chelp = fields.Char(u'chelp')
    cexch_name = fields.Char(u'cexch_name')
    cmeasure = fields.Char(u'cmeasure')
    bperson = fields.Boolean(u'bperson')
    bcus = fields.Boolean(u'bcus')
    bsup = fields.Boolean(u'bsup')
    bdept = fields.Boolean(u'bdept')
    bitem = fields.Boolean(u'bitem')
    cass_item = fields.Char(u'cass_item')
    br = fields.Boolean(u'br')
    be = fields.Boolean(u'be')
    cgather = fields.Char(u'cgather')
    bend = fields.Boolean(u'bend')
    bexchange = fields.Boolean(u'bexchange')
    bcash = fields.Boolean(u'bcash')
    bbank = fields.Boolean(u'bbank')
    bused = fields.Boolean(u'bused')
    bd_c = fields.Boolean(u'bd_c')
    dbegin = fields.Datetime(u'dbegin')
    dend = fields.Datetime(u'dend')
    itrans = fields.Integer(u'itrans')
    bclose = fields.Boolean(u'bclose')
    cother = fields.Char(u'cother')
    iotherused = fields.Integer(u'iotherused')
    bc_define1 = fields.Boolean(u'bcDefine1')
    bc_define2 = fields.Boolean(u'bcDefine2')
    bc_define3 = fields.Boolean(u'bcDefine3')
    bc_define4 = fields.Boolean(u'bcDefine4')
    bc_define5 = fields.Boolean(u'bcDefine5')
    bc_define6 = fields.Boolean(u'bcDefine6')
    bc_define7 = fields.Boolean(u'bcDefine7')
    bc_define8 = fields.Boolean(u'bcDefine8')
    bc_define9 = fields.Boolean(u'bcDefine9')
    bc_define10 = fields.Boolean(u'bcDefine10')
    bc_define11 = fields.Boolean(u'bcDefine11')
    bc_define12 = fields.Boolean(u'bcDefine12')
    bc_define13 = fields.Boolean(u'bcDefine13')
    bc_define14 = fields.Boolean(u'bcDefine14')
    bc_define15 = fields.Boolean(u'bcDefine15')
    bc_define16 = fields.Boolean(u'bcDefine16')
    i_view_item = fields.Integer(u'iViewItem')
    b_gcjs = fields.Boolean(u'bGCJS')
    b_cash_item = fields.Boolean(u'bCashItem')
    pubufts = fields.Binary(u'pubufts')
    b_report = fields.Boolean(u'bReport')
    c_user_define_type = fields.Char(u'cUserDefineType')
    iyear = fields.Integer(u'iyear')
    d_modify_date = fields.Datetime(u'dModifyDate')
    b_generate = fields.Boolean(u'bgenerate')
    bungenerate = fields.Boolean(u'bungenerate')
    bcykm = fields.Boolean(u'bcykm')

