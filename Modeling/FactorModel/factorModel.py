import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import ffm
import xlsxwriter

fm = ffm.ffm('20150831','20170831','20170927')
fm.modeling(['S102306','S102306'], 10)

print(fm.rSeries)
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