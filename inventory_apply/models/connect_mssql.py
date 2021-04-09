# -*- coding: utf-8 -*-
# sqlserver的连接
import pymssql

from odoo.exceptions import ValidationError


class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __getConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise ValidationError("没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise ValidationError("连接数据库失败")
        else:
            return cur

    def execQuery(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        """
        cur = self.__getConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def execNonQuery(self, sql):
        """
        执行非查询语句

        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__getConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


def main():
    ms = MSSQL(host="192.168.0.28:1433", user="sa", pwd="1", db="UFDATA_001_2020")
    resList = ms.execQuery("""SELECT * FROM warehouse""")
    print(resList)


if __name__ == '__main__':
    main()
