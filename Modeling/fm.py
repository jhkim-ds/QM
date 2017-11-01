import sys, os
import numpy as np
import pandas as pd
import pyodbc
import pymysql
import pyq

class fm():
    def __init__(self):
        self.sqlInfo = 'DRIVER={SQL Server};SERVER=211.174.180.232;DATABASE=DaishinQuantDB;UID=quant;PWD=9uant'
        self.mysqlcon = pymysql.connect(host='172.17.2.100', port=3306, user='smkim', passwd='smkim', db='smk',charset='utf8')

        self.conn = pyodbc.connect(self.sqlInfo)
        self.cursor = self.conn.cursor()
        self.rowData = ''
        self.scoredData = ''
        self.pyq = pyq.pyq()

    def univ(self, dt):
        row = self.pyq.univ(dt)

        dt = []
        code = []
        nm = []
        wics = []
        cap = []
        while row:
            dt.append(row[0])
            code.append(row[1])
            nm.append(row[2])
            wics.append(row[3])
            cap.append(row[4])
            row = self.pyq.cursor.fetchone()

        df = pd.DataFrame({'DT1': dt, 'CODE': code, 'NAME': nm, 'WICSBIG': wics, 'CAP': cap},
                          columns=['DT1', 'CODE', 'NAME', 'WICSBIG', 'CAP'])

        return df

    def factor(self, df, item, type='raw'):
        if type == 'raw':
            if item[0] == 'S':
                res = pd.read_sql("SELECT stk_cd, val FROM smk.stock_items where item_cd='%s' and period='%s'" % (item, list(set(df['DT1'].tolist()))[0]), self.mysqlcon)
            else:
                res = pd.read_sql("SELECT stk_cd, val FROM smk.consensus_items where item_cd='%s' and period='%s'" % (item, list(set(df['DT1'].tolist()))[0]), self.mysqlcon)
        else:
            if item[0] == 'S':
                res = pd.read_sql("SELECT stk_cd, val FROM smk.stock_items where item_cd='%s' and period='%s'" % (item, list(set(df['DT1'].tolist()))[0]), self.mysqlcon)

                if item in ['S503100.M', 'S503300.M']:
                    res['val'] = 1/res['val']

            else:
                res = pd.read_sql("SELECT stk_cd, val FROM smk.consensus_items where item_cd='%s' and period='%s'" % (item, list(set(df['DT1'].tolist()))[0]), self.mysqlcon)

        df = df.merge(res, left_on='CODE', right_on='stk_cd', how='left')
        df = self.pyq.factor(df, item)

        return df

    def scoring(self, df, fnum):
        for i in range(fnum-1):
            df[['sf%s' % str(i + 1)]] = df[['f%s' % str(i + 1)]].apply(lambda x: (x-x.mean()) / x.std())
            df['sf%s' % str(i + 1)].fillna(0, inplace=True)

        return df

    def getSum(self, df, fnum):
        df['total'] = 0
        df = self.pyq.getSum(df, fnum)

        return df

    def port(self, df, num, name):
        if num > 0:
            df = df.sort_values([name], ascending=False).reset_index(drop=True)
        else:
            df = df.sort_values([name], ascending=True).reset_index(drop=True)

        if name == 'total':
            del df[name]

        return df[df.index<abs(num)]

    def calR(self, df, dt2):
        df['DT2'] = dt2
        dt1 = list(set(df['DT1'].tolist()))[0]
        res = self.pyq.calR(df, dt2)
        res = res.set_index(['period', 'stk_cd']).unstack(1)
        res.columns = res.columns.droplevel(0)
        res.fillna(method='ffill', inplace=True)
        stockPrice = res.copy().transpose()

        temp = stockPrice[[dt1]]
        temp2 = stockPrice[[dt2]]
        df['PRICE1'] = None
        df['PRICE2'] = None
        for c in df['CODE'].tolist():
            df.loc[df['CODE'] == c, 'PRICE1'] = float(temp.loc[temp.index == c, dt1])
            df.loc[df['CODE'] == c, 'PRICE2'] = float(temp2.loc[temp.index == c, dt2])

        df['R'] = df['PRICE2'] / df['PRICE1'] - 1

        return df
