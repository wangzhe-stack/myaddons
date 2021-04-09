# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api


class DeptReport(models.Model):
    _name = "dept.report"
    _description = "Dept Report"
    _auto = False

    c_dept_code = fields.Char("C_DEPT_CODE")
    c_dept_name = fields.Char("C_DEPT_NAME")
    i_all_money = fields.Float("I_ALL_MONEY", digits=(15, 4))
    i_money = fields.Float("I_MONEY", digits=(15, 4))

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)

        self._cr.execute("""
        CREATE OR REPLACE VIEW {} AS (
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
             t1.c_share_kind_code = 'sys01' 
             AND t2.c_year = '2019' 
             AND t3.c_year = '2019' 
            GROUP BY
             t1.c_dept_code,
             t1.c_dept_name 
            ORDER BY
             t1.c_dept_code ASC)                        
        """.format(self._table))
