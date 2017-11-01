import fm
import dt
import pandas as pd

class ffm():
    def __init__(self, dt1, dt2, today=None):
        self.cdt = dt.dt()
        self.dtList = self.cdt.getDt(dt1,dt2)
        self.today = today
        if self.today != None:
            self.dtList.append(today)
        self.rowData = []
        self.scoredData = []
        self.port = []

    def modeling(self, f, num, type='raw'):
        r = []
        d = []
        d2 = []
        for i in range(len(self.dtList)-1):
            p = fm.fm()
            df = p.univ(self.dtList[i]).copy()
            for ft in f:
                df = p.factor(df,ft, type).copy()

            df = p.scoring(df, p.pyq.fnum).copy()
            df = p.getSum(df, p.pyq.fnum).copy()
            df = p.port(df, num, 'total').copy()
            df = p.calR(df, self.dtList[i+1]).copy()
            d.append(self.dtList[i])
            d2.append(self.dtList[i+1])
            r.append(df['R'].mean())
            self.rowData.append(p.pyq.rowData.copy())
            self.scoredData.append(p.pyq.scoredData.copy())
            self.port.append(df.copy())

        self.rSeries = pd.DataFrame({'dt1':d, 'dt2':d2, 'r':r})

    def weekly(self):
        self.dtWeekList = self.cdt.getWeekDt(dt1, dt2)
        if self.today != None:
            self.dtWeekList.append(self.today)

        print(self.dtWeekList)


dt1 = '20170331'
dt2 = '20170831'
dt3 = '20170927'

fms = ffm(dt1, dt2, dt3)
fms.modeling(['S503100.M'], 30, 'not raw')
print(fms.weekly())
print(fms.rSeries)