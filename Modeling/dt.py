import sys, os
import numpy as np
import pandas as pd
import pyodbc
import pymysql

class dt():
    def __init__(self):
        self.sqlInfo = 'DRIVER={SQL Server};SERVER=211.174.180.232;DATABASE=DaishinQuantDB;UID=quant;PWD=9uant'
        self.mysqlcon = pymysql.connect(host='172.17.2.100', port=3306, user='smkim', passwd='smkim', db='smk',charset='utf8')

        self.conn = pyodbc.connect(self.sqlInfo)
        self.cursor = self.conn.cursor()

    def getDt(self, dt1, dt2):
        string = "select YMD from wfns2db.dbo.tz_date where TRADE_YN='1' and MNO_OF_YR in ('3','5','8','11') AND MN_END_YN='1' AND YMD>='%s' AND YMD<='%s'" % (dt1, dt2)
        self.cursor.execute(string)
        row = self.cursor.fetchone()

        dt = []
        while row:
            dt.append(row[0])
            row = self.cursor.fetchone()

        return dt

    def getWeekDt(self, dt1, dt2):
        string = "select YMD from wfns2db.dbo.tz_date where TRADE_YN='1' and (MNO_OF_YR in ('3','5','8','11') AND MN_END_YN='1' or wk_END_YN='1') AND YMD>='%s' AND YMD<='%s'" % (dt1, dt2)
        self.cursor.execute(string)
        row = self.cursor.fetchone()

        dt = []
        while row:
            dt.append(row[0])
            row = self.cursor.fetchone()

        return dt