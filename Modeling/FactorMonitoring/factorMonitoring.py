import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import ffm
import datetime
import xlsxwriter

dt1 = '20160831'
dt2 = '20170831'
dt3 = '20170927'
t1 = datetime.datetime.now()
print(t1)

st = ['P/E(Fwd.12M)','P/B(Fwd.12M)','EPS(Fwd.12M) 변화율']
f = [['S503100.M'],['S503300.M'],['E311960']]

xx = 0
yy = 0
workbook = xlsxwriter.Workbook('m.xlsx')
worksheet = workbook.add_worksheet('monitoring')
worksheet.write_column(xx+1,yy, list(st))

for w in range(len(f)):
    fm = ffm.ffm(dt1,dt2,dt3)
    fm.modeling(f[w], 30, 'not raw')

    if w == 0:
        worksheet.write_row(xx,yy+1, list(fm.rSeries['dt2']))

    worksheet.write_row(xx+w+1, yy+1, fm.rSeries['r']*100)

t2 = datetime.datetime.now()

workbook.close()

print(t2)
print(t2-t1)

# print(fm.rowData[0])
# print(fm.scoredData[0])
# print(fm.port)

# workbook = xlsxwriter.Workbook('result.xlsx')
# worksheet = workbook.add_worksheet('port')
# worksheet.write_row(0,0, list(fm.port[0].columns))
# index = 1
# for i in range(len(fm.port)):
#     colList = list(fm.port[0].columns)
#     for c in range(len(colList)):
#         worksheet.write_column(index,c, list(fm.port[i][colList[c]]))
#
#     index += len(fm.port[i].index)
#
# worksheet = workbook.add_worksheet('r')
# worksheet.write_row(0,0, list(fm.rSeries.columns))
# index = 1
# colList = list(fm.rSeries.columns)
# for c in range(len(colList)):
#     worksheet.write_column(index,c, list(fm.rSeries[colList[c]]))
#
# workbook.close()