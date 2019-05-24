from ts import *
from evaluator import *

def simpleExponentialSmoothing(observedData, alpha):
    predictedData = observedData[:]
    for i in range(1, len(observedData)):
        predictedData[i] = (1 - alpha) * predictedData[i-1] + alpha * observedData[i-1]
    return (1 - alpha) * predictedData[-1] + alpha * observedData[-1]

def hourlyES(ts, alpha, pivot):

    indexs = ts.getIndexList()
    res = []

    length = len(ts.getDataList())

    for i in range(pivot, length-1):
        timestamp = indexs[i]
        hr = timestamp.hour
        tstmp = ts.filterTime(end=timestamp)
        tstmp = tstmp.getIntervalListByHour(hr)
        obData = tstmp.getDataList()
        res.append(simpleExponentialSmoothing(obData, alpha))

    tsEndPart = ts.filterTime(start=indexs[pivot+1])
    evalData = tsEndPart.getDataList()

    print('MAPE is', getMAPE(evalData, res))

    return res

def hourlyMain(ts, alpha):
    length = float(len(ts.getDataList()))
    startPoint = input('Please give a number to start from ' + str(int(length * 2 / 3)) + ' to ' + str(int(length)))
    res = hourlyES(ts, alpha, int(startPoint))
    colName = 'ies a=' + str(alpha)
    ts.addCol(res, colName)
    ts.plot()
    ts.export('ies.txt')

def dailyES(ts, alpha, pivot):

    indexs = ts.getIndexList()
    res = []

    length = len(ts.getDataList())

    for i in range(pivot, length-1):
        timestamp = indexs[i]
        dayOfWeek = timestamp.weekday()
        tstmp = ts.filterTime(end=timestamp)
        tstmp = tstmp.getIntervalListByDay(dayOfWeek)
        obData = tstmp.getDataList()
        res.append(simpleExponentialSmoothing(obData, alpha))

    tsEndPart = ts.filterTime(start=indexs[pivot+1])
    evalData = tsEndPart.getDataList()

    print('MAPE is', getMAPE(evalData, res))

    return res

def dailyMain(ts, alpha):
    ts = ts.setIntervalLength('day')
    length = float(len(ts.getDataList()))
    startPoint = input('Please give a number to start from ' + str(int(length * 2 / 3)) + ' to ' + str(int(length)))
    res = dailyES(ts, alpha, int(startPoint))
    colName = 'ies a=' + str(alpha)
    ts.addCol(res, colName)
    ts.plot()
    ts.export('ies.txt')


def main():
    fileName = input('Please input the data file name:')
    ts = TimeSeriesData.readTsFile(fileName)
    interval = input('Please input the interval (day/hour):')
    alpha = input('Please input alpha value (0,1):')
    if interval == 'day':
        dailyMain(ts, float(alpha))
    else:
        hourlyMain(ts, float(alpha))


if __name__ == '__main__':
    main()
