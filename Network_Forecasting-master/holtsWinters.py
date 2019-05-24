from __future__ import division
from ts import *
from evaluator import *


def additive(values, periodicity, forecastLength, alpha, beta, gamma):
    Y = values[:]
    a = [sum(Y[0:periodicity]) / float(periodicity)]
    b = [(sum(Y[periodicity:2 * periodicity]) - sum(Y[0:periodicity])) / periodicity ** 2]
    s = [Y[i] - a[0] for i in range(periodicity)]
    y = [a[0] + b[0] + s[0]]

    for i in range(len(Y) + forecastLength):
        if i == len(Y):
            Y.append(a[-1] + b[-1] + s[-periodicity])
        a.append(alpha * (Y[i] - s[i]) + (1 - alpha) * (a[i] + b[i]))
        b.append(beta * (a[i + 1] - a[i]) + (1 - beta) * b[i])
        s.append(gamma * (Y[i] - a[i] - b[i]) + (1 - gamma) * s[i])
        y.append(a[i + 1] + b[i + 1] + s[i + 1])

    return Y[-forecastLength:]


def multiplicative(values, periodicity, forecastLength, alpha, beta, gamma):
    Y = values[:]
    a = [sum(Y[0:periodicity]) / float(periodicity)]
    b = [(sum(Y[periodicity:2 * periodicity]) - sum(Y[0:periodicity])) / periodicity ** 2]
    s = [Y[i] / a[0] for i in range(periodicity)]
    y = [(a[0] + b[0]) * s[0]]

    for i in range(len(Y) + forecastLength):
        if i == len(Y):
            Y.append((a[-1] + b[-1]) * s[-periodicity])
        a.append(alpha * (Y[i] / s[i]) + (1 - alpha) * (a[i] + b[i]))
        b.append(beta * (a[i + 1] - a[i]) + (1 - beta) * b[i])
        s.append(gamma * (Y[i] / (a[i] + b[i])) + (1 - gamma) * s[i])
        y.append((a[i + 1] + b[i + 1]) * s[i + 1])
    return Y[-forecastLength:]


ts = TimeSeriesData.readTsFile("internet-traffic-data-20041119-20050127.csv")
ts.plot()
values = ts.getDataList()
print(values)
trainPivot = 24
print('pivot is ' + str(trainPivot))
values = values[:-trainPivot]
res = multiplicative(values, 24, trainPivot, 0.01, 0.01, 0.01)
print(res)
print(len(res))
ts.addCol(res ,"holtwintersmultiplicitve")
ts.plot()
print(ts)
ts.export('res.txt')






# multiplicative()
