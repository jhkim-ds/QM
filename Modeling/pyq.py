import numpy as np
import pandas as pd
import pyodbc
import pymysql

class pyq():
    def __init__(self):
        self.sqlInfo = 'DRIVER={SQL Server};SERVER=211.174.180.232;DATABASE=DaishinQuantDB;UID=quant;PWD=9uant'
        self.mysqlcon = pymysql.connect(host='172.17.2.100', port=3306, user='smkim', passwd='smkim', db='smk',
                                        charset='utf8')

        self.conn = pyodbc.connect(self.sqlInfo)
        self.cursor = self.conn.cursor()
        self.fnum = 1
        self.rowData = ''
        self.scoredData = ''

    def univ(self, dt):
        string = "select b.TRD_DT, 'A' + b.stk_cd stk_cd, b.stk_nm_kor, d.SEC_NM_KOR 'wicsBig', e.mkt_val \
                      from WFNS2DB.dbo.TZ_DATE a, WFNS2DB.dbo.TS_STK_ISSUE b, WFNC2DB.dbo.TC_COMPANY c, WFNC2DB.dbo.TC_SECTOR d, WFNS2DB.dbo.TS_STK_DAILY e where a.ymd = b.TRD_DT and b.stk_cd = c.CMP_CD and substring(c.gics_cd,1,3) = d.SEC_CD and b.STK_CD = e.stk_cd \
    	              and b.TRD_DT = e.TRD_dt and a.ymd = '%s' and b.KS200_TYP = 1 order by MKT_VAL desc" % dt

        self.cursor.execute(string)
        row = self.cursor.fetchone()

        return row

    def factor(self, df, item):
        df.rename(columns={'val': 'f%s' % self.fnum}, inplace=True)
        del df['stk_cd']
        self.rowData = df

        self.fnum += 1
        return df

    def getSum(self, df, fnum):
        for i in range(fnum - 1):
            df['total'] += df['sf%s' % str(i + 1)]
            del df['sf%s' % str(i + 1)]
        self.scoredData = df.copy()

      
        return df

    def calR(self, df, dt2):
        dt1 = list(set(df['DT1'].tolist()))[0]
        res = pd.read_sql("SELECT * FROM smk.stk_hist where period>='%s' and period<='%s'" % (dt1, dt2), self.mysqlcon)
        return res
