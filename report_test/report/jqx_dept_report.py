# -*- coding: utf-8 -*-
from odoo import api, fields, models


class JQXDeptReport(models.Model):
    _name = "jqx.dept.report"
    _description = "jqx.dept.report"
    _auto = False

    @api.model
    def get_data(self, year=None, sys=None):
        if not year:
            year = 2019
        if not sys:
            sys = 'sys01'
        sql = """
            SELECT
             min(t1.id) as id,
             t1.c_dept_code,
             t1.c_dept_name,
             SUM ( t2.i_all_money ) AS i_all_money,
             SUM ( t3.i_money ) AS i_money 
            FROM
             EF_Cost_Dept t1
             LEFT JOIN (
             SELECT
              c_year,
              c_dept_code,
              SUM ( i_all_money ) AS i_all_money 
             FROM
              EF_cost_CostShare where c_cost_item_code not in ('402','502')
             GROUP BY
              c_year,
              c_dept_code 
             ) t2 ON t1.c_dept_code = t2.c_dept_code
             LEFT JOIN (
             SELECT
              i.c_year,
              k.c_order_dept_code,
              SUM ( k.i_money ) AS i_money 
             FROM
              EF_cost_incmDataM i
              LEFT JOIN EF_Cost_ChargeKindData k ON i.i_id = k.i_id 
             GROUP BY
              i.c_year,
              k.c_order_dept_code 
             ) t3 ON t1.c_dept_code = t3.c_order_dept_code 
            WHERE
             t1.c_share_kind_code = '{0}'
             AND t2.c_year = '{1}'
             AND t3.c_year = '{1}'
            GROUP BY
             t1.c_dept_code,
             t1.c_dept_name 
            ORDER BY
             t1.c_dept_code ASC
        """.format(sys, year)
        self.env.cr.execute(sql)
        dicts = self.env.cr.dictfetchall()
        return dicts
