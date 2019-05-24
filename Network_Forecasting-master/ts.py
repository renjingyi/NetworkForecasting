import pandas as pd
import matplotlib.pyplot as plt

class TimeSeriesData:

    def __init__(self, ts):
        self.ts = ts

    @classmethod
    def readTsFile(cls, fileName):
        headers = ['DateTime', 'ObservedValue']
        ts = pd.read_csv(fileName, sep=',', header=None, names=headers)
        ts['DateTime'] = pd.to_datetime(ts['DateTime'], format='%Y-%m-%d %H:%M:%S')
        ts.index = ts['DateTime']
        del ts['DateTime']
        return TimeSeriesData(ts)

    def __repr__(self):
        return self.ts.__repr__()

    def getTs(self):
        return self.ts

    def addCol(self, dataList, colName):
        ts = self.ts
        if len(dataList) < len(ts.index):
            num = len(ts.index) - len(dataList)
            headEmptyList = [None] * num
            dataList = headEmptyList + dataList
        self.ts[colName] = dataList

    def plot(self):
        self.ts.plot()
        plt.show()

    def export(self, fileName):
        self.ts.to_csv(fileName, sep=',', encoding='utf-8')

    def getIntervalLength(self):
        indexs = self.ts.index.tolist()
        interval = None
        if len(indexs) > 1:
            interval = indexs[1] - indexs[0]
        return interval

    def getStartInterval(self):
        return self.ts.index[0]

    def getEndInterval(self):
        return self.ts.index[-1]

    def filterTime(self, start=None, end=None):
        if start == None:
            start = str(self.getStartInterval())
        if end == None:
            end = str(self.getEndInterval())
        return TimeSeriesData(self.ts.ix[start:end])

    def setIntervalLength(self, interval=None):
        ts = self.ts
        if interval == 'day':
            ts = ts.resample('D').sum()
        elif interval == 'week':
            ts = ts.resample('W').sum()
        return TimeSeriesData(ts)

    def getDataList(self, valueName = 'ObservedValue'):
        return self.ts[valueName].tolist()

    def getIndexList(self):
        return self.ts.index.tolist()

    def getIntervalListByHour(self, index):
        hour = self.ts.index.hour
        selector = (hour == index)
        data = self.ts[selector]
        return TimeSeriesData(data)

    def getIntervalListByDay(self, index):
        ts = self.setIntervalLength('day')
        dayOfWeek = ts.getTs().index.weekday
        selector = (dayOfWeek == index)
        data = ts.getTs()[selector]
        return TimeSeriesData(data)

