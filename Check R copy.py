import urllib.request
import csv
import numpy as np
from scipy.stats.stats import pearsonr
from datetime import date, datetime, timedelta
import pandas_datareader.data as web
import pandas as pd
import sys

Tickers=[]
newTickers=[]
baseData = []
#currData = []

TickerCount = 0
IncrementCount = 0
i = 0
j = 0
k = 0
m = 0
df = pd.DataFrame()

currFile = "ETFs.csv"
currData = list(csv.reader(open(currFile, 'rU'), dialect=csv.excel_tab))
TickerCount = len(currData)
Tickers = np.array(currData).flatten().tolist()

print (Tickers)
print (TickerCount)

#date_entry = input('Begin date in YYYY-MM-DD format:')
date_entry = "2017-01-10"
year, month, day = map(int, date_entry.split('-'))
NBegDate = datetime(year, month, day)
#date_entry = input('End date in YYYY-MM-DD format:')
date_entry = "2017-06-07"
year, month, day = map(int, date_entry.split('-'))
NEndDate = datetime(year, month, day)


#resultMatrix = np.zeros((TickerCount, TickerCount))
resultMatrix = []

for i in range(0, TickerCount):
    try:
        f = web.DataReader(Tickers[i], 'google', NBegDate, NEndDate)
        df = f['Close']
        row = df.values
        if row.any() and row.all():
            row = np.transpose(row)
            baseData.append(row)
            newTickers.append(Tickers[i])
            print(Tickers[i])
    except:
        next

baseData = np.matrix(baseData)
shiftedbaseData = baseData[:, 1:]
shiftedbaseData2 = baseData[:, 0:-1]
returnData = shiftedbaseData-shiftedbaseData2
returnData = np.divide(returnData,shiftedbaseData2)


print('get ok')

i = 0
j = 0
TickerCount = len(newTickers)
for i in range(0, TickerCount):
    currR=[]
    j=0
    for j in range(0, TickerCount):
        row_i = returnData[i, :]
        row_i = np.array(row_i)[0].tolist()
        #print(row_i)
        row_j = returnData[j, :]
        row_j = np.array(row_j)[0].tolist()
        s = pearsonr(row_i, row_j)[0]
        currR.append(s)
    resultMatrix.append(currR)

resultMatrix = np.matrix(resultMatrix)
#print(np.size(resultMatrix))

i = 0
while i < TickerCount:
    j = 0
    while j < TickerCount:
        if j != i:
            if abs(resultMatrix.item(i,j)) > 0.15:
                #print(resultMatrix[i][j])
                resultMatrix = np.delete(resultMatrix, j, 1)
                resultMatrix = np.delete(resultMatrix, j, 0)
                newTickers = np.delete(newTickers, j, 0)
                if j < i:
                    i = i - 1
                j = j - 1
                TickerCount = TickerCount - 1
                #print(newTickers)
                #print(resultMatrix)
        j = j + 1
    i = i + 1


np.savetxt('Results.csv', resultMatrix, delimiter=',')
#with open("Results.csv", "w") as wt:
#    writer = csv.writer(wt)
#    writer.writerows(resultMatrix)

with open("EFS.csv", "w") as wt:
    writer = csv.writer(wt)
    writer.writerows(newTickers)
