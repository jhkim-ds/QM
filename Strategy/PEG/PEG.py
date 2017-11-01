import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import ffm
import pandas as pd
import xlsxwriter

dt1 = '20110831'
dt2 = '20170831'
td = '20171025'

fm = ffm.ffm(dt1, dt2, td)
dtList = fm.dtList
ffm = ffm.fm.fm()
r = [0]
d = [dt1]
d2 = [dt1]
port1 = []
port2 = []

for i in range(len(dtList)-1):
    df = ffm.univ(dtList[i])
    ffm.pyq.fnum = 1
    df = ffm.factor(df, 'S503100.M')
    df = ffm.factor(df, 'S503300.M')
    df = ffm.factor(df, 'E311960')
    df = df.rename(columns={'f1': 'PER', 'f2': 'PBR', 'f3': 'EPS Growth'})
    df = df[(df['CAP']>=500000000000) & ((df['PER']<10) | (df['PBR']<1))]
    df['PEG'] = df['PER'] / df['EPS Growth']
    df = df.dropna(axis=0, how='any')
    df = ffm.calR(df, dtList[i+1])
    d.append(dtList[i])
    d2.append(dtList[i + 1])

    df = df[(df['EPS Growth'] > 0) & (df['PER'] > 0)]

    df1 = ffm.port(df, -30, 'PEG')

    port1.append(df1)
    port2.append(df1)
    r.append(df1['R'].mean() * 100)
    # r.append((df1['R'].mean()-df2['R'].mean())*100)

rSeries = pd.DataFrame({'dt1': d, 'dt2': d2, 'r': r})
print(rSeries)

workbook = xlsxwriter.Workbook('result.xlsx')
worksheet = workbook.add_worksheet('port1')
worksheet.write_row(0,0, list(port1[0].columns))
index = 1
for i in range(len(port1)):
    colList = list(port1[0].columns)
    for c in range(len(colList)):
        worksheet.write_column(index,c, list(port1[i][colList[c]]))
    index += len(port1[i].index)
worksheet = workbook.add_worksheet('port2')
worksheet.write_row(0,0, list(port2[0].columns))
index = 1
for i in range(len(port2)):
    colList = list(port2[0].columns)
    for c in range(len(colList)):
        worksheet.write_column(index,c, list(port2[i][colList[c]]))
    index += len(port2[i].index)
worksheet = workbook.add_worksheet('r')
worksheet.write_row(0,0, list(rSeries.columns))
index = 1
colList = list(rSeries.columns)
for c in range(len(colList)):
    worksheet.write_column(index,c, list(rSeries[colList[c]]))

workbook.close()
