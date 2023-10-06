import csv

import requests
import datetime
from nse import Nse
import numpy as np
import pandas as pd

nse = Nse()

headers = {'Accept': '*/*',
           'Accept-Language': 'en-US,en;q=0.5',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest',
           'Authority': 'www.nseindia.com'
           }


def getAllStocksSymbols():
    stocksList = nse.get_stock_codes()
    del stocksList['SYMBOL']
    return stocksList


def getAllHistoricalDataCsv(symbol, fromDate, toDate):
    baseUrl = 'https://www.nseindia.com/api/historical/cm/equity?symbol=%s&series=["EQ"]&from=%s&to=%s&csv=true'
    url = baseUrl % (symbol, fromDate, toDate)

    headers = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.5',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest',
               'Authority': 'www.nseindia.com'
               }
    s = requests.Session()
    s.get("http://www.nseindia.com/", headers=headers)
    data = s.get(url, headers=headers)
    return data


def getAllHistoricalData(symbol, fromDate, toDate):
    baseUrl = 'https://www.nseindia.com/api/historical/cm/equity?symbol=%s&series=["EQ"]&from=%s&to=%s'
    url = baseUrl % (symbol, fromDate, toDate)
    s = requests.Session()
    s.get("http://www.nseindia.com/", headers=headers)
    data = s.get(url, headers=headers)
    return data.json()


def extractClosingPriceFromHistoricalData(data):
    closingPrices = []
    for price in data["data"]:
        closingPrices.append(price["CH_CLOSING_PRICE"])
    return closingPrices


def getHistoricalData(symbol, delta):
    d1 = datetime.date.today().strftime("%d-%m-%Y")
    d2 = (datetime.datetime.now() - datetime.timedelta(delta)).date().strftime("%d-%m-%Y")
    download = getAllHistoricalDataCsv(symbol, d2, d1)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    my_list.pop(0)
    data = []
    for row in my_list:
        data.append(float(row[7].replace(',', '')))
    data.reverse()
    if checkMarketStatus():
        livePrice = getLive(symbol=symbol)
        data.append(livePrice)
    return data


def calculateEma(data, period):
    if len(data) <= 30:
        return None
    window_size = period
    numbers_series = pd.Series(data)
    windows = numbers_series.rolling(window_size)
    moving_averages = windows.mean()
    moving_averages_list = moving_averages.tolist()
    sma = moving_averages_list[window_size - 1:]
    modPrice = pd.Series(data[period - 1:])
    modPrice.iloc[0:1] = sma[0:1]
    emaalt = modPrice.ewm(span=period, adjust=False).mean()
    finalData = np.round(emaalt, decimals=3)
    return finalData


def calFastMACD(symbol):
    data = getHistoricalData(symbol, 200)
    longEMA = calculateEma(data, 26)
    shortEMA = calculateEma(data[14:], 12)
    if pd.Series(longEMA).empty or pd.Series(shortEMA).empty:
        return None
    macd = shortEMA - longEMA
    macd = pd.Series(macd).tolist()
    macd.reverse()
    return macd


#
#
def calSlowMACD(symbol):
    data = getHistoricalData(symbol, 200)
    longEMA = calculateEma(data, 26)
    shortEMA = calculateEma(data[14:], 12)
    if pd.Series(longEMA).empty or pd.Series(shortEMA).empty:
        return None
    macd = shortEMA - longEMA
    slowMacdList = pd.Series(calculateEma(macd, 9)).tolist()
    slowMacdList.reverse()
    return slowMacdList


def checkMarketStatus():
    status = requests.get("https://www1.nseindia.com//emerge/homepage/smeNormalMktStatus.json", headers=headers)
    if status.json()['NormalMktStatus'] == 'closed':
        return False
    else:
        return True


def getLive(symbol):
    nse.get_quote(symbol, True)['lastPrice']


def getTickerTapeSymbol(symbol):
    response = requests.get(
        "https://api.tickertape.in/search?text=" + symbol + "&types=stock,brands,index,etf,mutualfund")
    if response.status_code == 200:
        resp = response.json()
        for s in resp['data']['stocks']:
            if s['ticker'] == symbol:
                return s['sid']
    return None


def getTickerTapeInfo(symbol):
    symb = getTickerTapeSymbol(symbol)
    if symb != None:
        response = requests.get("https://api.tickertape.in/stocks/info/" + symb)
        return response.json()
    return None


def getTickerTapeRecos(symbol):
    symb = getTickerTapeSymbol(symbol)
    if symb != None:
        response = requests.get("https://api.tickertape.in/stocks/reco/" + symb)
        return response.json()
    return None

# print(getTickerTapeRecos('HDFC'))
# print(checkMarketStatus())
# print(calFastMACD('INFY'))
# print(calSlowMACD('INFY'))
# print(len(calFastMACD('HDFCBANK')))
# print(len(calSlowMACD('HDFCBANK')))

# print(getAllStocksSymbols())
