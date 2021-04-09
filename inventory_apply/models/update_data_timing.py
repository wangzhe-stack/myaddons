import logging

from .connect_mssql import MSSQL
from odoo import models, api

_logger = logging.getLogger(__name__)


class UpdateDataTiming(models.Model):
    _name = 'update.data.timing'
    _description = "定时更新数据"

    ms = MSSQL(host="192.168.0.28:1433", user="sa", pwd="1", db="UFDATA_001_2020")

    @api.model
    def cearte_or_unlink(self, sql, model, fieldsList):
        """
        根据服务器 和 odoo 中的数据差异，同步数据，决定新增还是删除
        (由于res[0],所以查询第一个元素是code)
        :param sql: sql
        :param model: odoo模型
        :param fieldsList: 生成的字典的key
        :return datas: 新增的数据列表
        """

        resList = self.ms.execQuery(sql)
        ourList = self.env[model].search_read([], ['code'])
        retSet = set(res[0] for res in resList)
        ourSet = set(our.get('code') for our in ourList)
        if retSet == ourSet:
            _logger.info(f'{model}, 数据没有差异')
            return

        unlinkCode = ourSet - retSet
        creatCode = retSet - ourSet
        if unlinkCode:  # 应该删除的
            _logger.error(f'{model}有要删除的数据, code 为{unlinkCode}')
            self.env[model].search([('code', 'in', list(unlinkCode))]).unlink()

        if creatCode:  # 应该新增的
            _logger.error(f'{model}有要新增的数据, code 为{creatCode}')
            datas = []
            for res in resList:
                if res[0] in (creatCode):
                    datas.append(dict(zip(fieldsList, res)))
            return datas

    @api.model
    def updateDepartMent(self):
        sql = """SELECT cDepCode,cDepName,cDepFullName FROM Department where  bDepEnd = 1 ORDER BY iDepOrder"""
        model = 'department'
        fieldsList = ['code', 'name', 'fullname']
        datas = self.cearte_or_unlink(sql, model, fieldsList)
        if datas:
            self.env[model].create(datas)

    @api.model
    def updatePerson(self):
        sql = """SELECT cPersonCode,cPersonName,cPersonPhone,cDepCode FROM Person """
        model = 'person'
        fieldsList = ['code', 'name', 'phone', 'department_id']
        datas = self.cearte_or_unlink(sql, model, fieldsList)
        if datas:
            for data in datas:
                departCode = data['department_id']
                department_id = self.env['department'].search([('code', '=', departCode)]).id
                data['department_id'] = department_id
            self.env[model].create(datas)

    @api.model
    def updateInventory(self):
        sql = """select a.cInvCode,a.cInvName,a.cInvStd,a.cComUnitCode,b.quantity as quantity from inventory AS a
         left join (select cInvCode,cWhCode,SUM(iQuantity) AS quantity from CurrentStock group by cInvCode,cWhCode) AS b 
         on a.cInvCode = b.cInvCode"""
        model = 'inventory'
        fieldsList = ['code', 'name', 'c_inv_std', 'computation_unit_id', 'stock_number']
        datas = self.cearte_or_unlink(sql, model, fieldsList)
        if datas:
            for data in datas:
                c_com_unit_code = data['computation_unit_id']
                computation_unit_id = self.env['computation.unit'].search([('code', '=', c_com_unit_code)]).id
                data['computation_unit_id'] = computation_unit_id
            self.env[model].create(datas)

    @api.model
    def updateComputationUnit(self):
        sql = """select cComunitCode,cComUnitName,iNumber from ComputationUnit where bMainUnit =1"""
        model = 'computation.unit'
        fieldsList = ['code', 'name', 'i_number']
        datas = self.cearte_or_unlink(sql, model, fieldsList)
        if datas:
            self.env[model].create(datas)

    @api.model
    def updateRdStyle(self):
        sql = """select cRdCode, cRdName from Rd_Style where bRdFlag = 0 and bRdEnd = 1"""
        model = 'rd.style'
        fieldsList = ['code', 'name']
        datas = self.cearte_or_unlink(sql, model, fieldsList)
        if datas:
            self.env[model].create(datas)

    @api.model
    def updateWarehouse(self):
        sql = """select cWhCode,cWhName,cDepCode from Warehouse"""
        model = 'ware.house'
        fieldsList = ['code', 'name','c_dep_code']
        datas = self.cearte_or_unlink(sql, model, fieldsList)
        if datas:
            self.env[model].create(datas)

    @api.model
    def updateStockNumber(self):
        ourList = self.env['inventory'].search_read([], ['code','stock_number'])
        ourSet = set((our.get('code'),our.get('stock_number')) for our in ourList)

        resList = self.ms.execQuery("""select a.cInvCode,b.quantity as quantity from inventory AS a
                left join (select cInvCode,cWhCode,SUM(iQuantity) AS quantity from CurrentStock group by cInvCode,cWhCode) AS b
                on a.cInvCode = b.cInvCode""")
        resSet= set((res[0], float( res[1] if res[1] else 0))  for res in resList)

        # 更新和sql Server数据库有差异的库存
        updateSet = ourSet.difference(resSet)
        for data in updateSet:
            for res in resList:
                if res[0] == data[0]:
                    self.env['inventory'].search([('code','=',data[0])]).update({'stock_number': res[1]})
