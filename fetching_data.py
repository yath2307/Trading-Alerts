import threading
import time
import datetime
import nse_tools
import whatsapp_notify
import mail_notify
import pandas as pd
import pytz

stocks = nse_tools.getAllStocksSymbols()

alertMapping = []

IST = pytz.timezone('Asia/Kolkata')

for stock in stocks:
    alertMapping.append(0)

breakit = False
def background(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def backgrnd_func(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return backgrnd_func

@background
def start():
    while True:
        i = 0
        for stock in stocks:
            if alertMapping[i] == 0:
                hour = datetime.datetime.now(IST).hour
                alertMapping[i] = (24+9-hour)
                fastMacd = nse_tools.calFastMACD(stock)
                slowMacd = nse_tools.calSlowMACD(stock)
                if fastMacd is None or slowMacd is None:
                    continue
                fastMacd = pd.Series(fastMacd)
                fastMacd = fastMacd[0:len(fastMacd) - 8]
                slowMacd = pd.Series(slowMacd)
                diff = fastMacd - slowMacd
                diff = diff.tolist()
                data = nse_tools.getHistoricalData(stock, 180)
                data.reverse()
                try:
                    signal1 = diff[0] <= 0
                    signal2 = (diff[0] < diff[1] < diff[2])
                    signal3 = ((max(data) - data[0])/data[0])*100 <= 2
                    if (signal1 or signal2) and signal3:
                        print('sell me andar aagye')
                        whatsapp_notify.send_message(stockName=stocks[stock], buy=False)
                        mail_notify.send_mail(stockName=stocks[stock], buy=False)
                except Exception as e:
                    print("sell wale me error aagyi yaar :-( ", e)
                try:
                    signal1 = diff[0] >= 0
                    signal2 = (diff[0] > diff[1] > diff[2])
                    signal3 = ((max(data) - data[0]) / data[0]) * 100 >= 10
                    reco = nse_tools.getTickerTapeRecos(stock)
                    signal4 = False
                    if reco is not None and reco['data'] is not None and reco['data']['percBuyReco'] is not None and reco['data']["totalReco"] is not None:
                        signal4 = reco['data']['percBuyReco'] >= 70
                    if (signal1 or signal2) and signal3 and signal4:
                        print('buy me andar aagye')
                        whatsapp_notify.send_message(stockName=stock, buy=True, reco=reco['data'])
                        mail_notify.send_mail(stockName=stock, buy=True, reco=reco['data'])
                except Exception as e:
                    print("buy wale me error aagyi yaar :-( ", e)
            alertMapping[i] -= 1
            i += 1
        global breakit
        if breakit:
            time.sleep(3600*24*7)
        time.sleep(3600)
def stop():
    global breakit
    breakit = True