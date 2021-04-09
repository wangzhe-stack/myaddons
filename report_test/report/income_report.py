# -*- coding: utf-8 -*-

from odoo import fields, models, tools


class IncomeReport(models.Model):
    _name = "income.report"
    _description = "Income Report"
    _auto = False

    ccode = fields.Char("ccode")
    cname = fields.Char("cname")
    je = fields.Float("je", digits=(15, 4))

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)

        self._cr.execute("""
            CREATE OR REPLACE VIEW {} AS (
                select 1 as id,'400101' as ccode,'财政基本收入' as cname,sum(case when t1.ccode like '400101%' 
                then t1.mc else 0.00 end) as je from gl_Accsum t1 left join code t2 on t1.ccode = t2.ccode and 
                t1.iyear =t2.iyear where t1.iyear = 2019 and t2.bend = true
                
                union ALL
                
                select 2 as id,'400102' as ccode,'财政项目收入' as cname,sum(case when t1.ccode like '400102%' 
                then t1.mc else 0.00 end) as je from gl_Accsum t1 left join code t2 on t1.ccode = t2.ccode and 
                t1.iyear =t2.iyear where t1.iyear = 2019 and t2.bend = true
                
                union ALL
                
                select 3 as id,'41010101' as ccode,'门诊收入' as cname,sum(case when t1.ccode like '41010101%' 
                then t1.mc else 0.00 end) as je from gl_Accsum t1 left join code t2 on t1.ccode = t2.ccode and 
                t1.iyear =t2.iyear where t1.iyear = 2019 and t2.bend = true
                
                union ALL
                
                select 4 as id,'41010102' as ccode,'住院收入' as cname,sum(case when t1.ccode like '41010102%' 
                then t1.mc else 0.00 end) as je from gl_Accsum t1 left join code t2 on t1.ccode = t2.ccode and 
                t1.iyear =t2.iyear where t1.iyear = 2019 and t2.bend = true
                
                union ALL
                
                select 5 as id,'41010103' as ccode,'结算差额' as cname,sum(case when t1.ccode like '41010103%' 
                then t1.mc else 0.00 end) as je from gl_Accsum t1 left join code t2 on t1.ccode = t2.ccode and 
                t1.iyear =t2.iyear where t1.iyear = 2019 and t2.bend = true
                
                union ALL
                
                select 6 as id,'410102' as ccode,'科教收入' as cname,sum(case when t1.ccode like '410102%' 
                then t1.mc else 0.00 end) as je from gl_Accsum t1 left join code t2 on t1.ccode = t2.ccode and 
                t1.iyear =t2.iyear where t1.iyear = 2019 and t2.bend = true
                
                union ALL
                
                select 7 as id,'4699' as ccode,'其他收入' as cname,sum(case when t1.ccode like '4201%' or  t1.ccode 
                like '4301%' or  t1.ccode like '4401%' or  t1.ccode like '46%' then t1.mc else 0.00 end) as je 
                from gl_Accsum t1 left join code t2 on t1.ccode = t2.ccode and t1.iyear =t2.iyear
                where t1.iyear = 2019 and t2.bend = true
            )
        """.format(self._table)
        )
