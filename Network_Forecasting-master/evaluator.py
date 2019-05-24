def getMAPE(actualData, forecastData):
    if len(actualData) != len(forecastData):
        raise Exception("the observe list and forecast list must has same length")
    size = len(actualData)
    percentageErrorSum = 0
    for i in range(size):
        if (actualData[i] == 0) or (forecastData[i] == None):
            size = size - 1
        else:
            percentageErrorSum += abs(actualData[i] - forecastData[i]) / actualData[i]
    return percentageErrorSum / size
