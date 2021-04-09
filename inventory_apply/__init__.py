# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID
from . import controllers
from . import models
from .models.connect_mssql import MSSQL


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    ms = MSSQL(host="192.168.0.28:1433", user="sa", pwd="1", db="UFDATA_001_2020")
    # 添加 计量单位
    resList = ms.execQuery("""select cComunitCode,cComUnitName,iNumber from ComputationUnit where bMainUnit =1""")
    datas = []
    for res in resList:
        cComunitCode, cComUnitName, iNumber = res
        datas.append({'code': cComunitCode, 'name': cComUnitName, 'i_number': iNumber})
    env['computation.unit'].create(datas)
    # 添加 出库分类
    resList = ms.execQuery(""" select cRdCode, cRdName from Rd_Style where bRdFlag = 0 and bRdEnd = 1""")
    datas = []
    for res in resList:
        code, name = res
        datas.append({'code': code, 'name': name})
    env['rd.style'].create(datas)
    # 添加 部门
    resList = ms.execQuery("""SELECT iDepOrder,cDepCode,cDepName,cDepFullName 
                      FROM Department where  bDepEnd = 1 ORDER BY iDepOrder""")
    datas = []
    for res in resList:
        id, code, name, fullname = res
        datas.append({'id': int(id), 'code': code, 'name': name, 'fullname': fullname})
    env['department'].create(datas)
    # 添加 业务员
    resList = ms.execQuery("""SELECT cPersonName,cPersonCode,cDepCode, cPersonPhone FROM Person """)
    datas = []
    for res in resList:
        name, code, departCode, phone = res
        department_id = env['department'].search([('code', '=', departCode)]).id
        datas.append({'name': name, 'code': code, 'department_id': department_id, 'phone': phone})
    env['person'].create(datas)
    # 添加 仓库
    resList = ms.execQuery(""" select cWhCode,cWhName,cDepCode from Warehouse""")
    datas = []
    for res in resList:
        cWhCode, cWhName, cDepCode = res
        datas.append({'code': cWhCode, 'name': cWhName, 'c_dep_code': cDepCode})
    env['ware.house'].create(datas)
    # 添加 物资
    resList = ms.execQuery("""select a.cInvCode,a.cInvName,a.cInvStd,a.cComUnitCode,b.quantity as quantity from inventory AS a
         left join (select cInvCode,cWhCode,SUM(iQuantity) AS quantity from CurrentStock group by cInvCode,cWhCode) AS b 
         on a.cInvCode = b.cInvCode""")
    datas = []
    for res in resList:
        cInvCode, cInvName, cInvStd, cComUnitCode, quantity = res
        computation_unit_id = env['computation.unit'].search([('code', '=', cComUnitCode)]).id
        datas.append({'code': cInvCode, 'name': cInvName, 'c_inv_std': cInvStd,
                      'computation_unit_id': computation_unit_id, 'stock_number': quantity})
    env['inventory'].create(datas)
