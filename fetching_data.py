import sys
import time
from datetime import date

import whatsapp_notify
import mail_notify

import requests

purchasedStocksList = ["HAL", "ADANIPORTS.BSE", "500180.BSE"]

toBePurchasedStocksList = []

breakit = False

def start():
    while True:
        for stock in purchasedStocksList:
            api_url = "https://www.alphavantage.co/query?function=MACD&symbol=" + stock + "&interval=daily&series_type=open&apikey=X51X1JMMQJUWY4SZ"
            response = requests.get(api_url)
            print(response)
            today = date.today()
            d1 = "20" + today.strftime("%y-%m-%d")
            try:
                latest_values = response.json()['Technical Analysis: MACD']['2021-08-20']
                print(latest_values)
                if latest_values['MACD'] <= latest_values['MACD_Signal']:
                    whatsapp_notify.send_message(stockName=stock, buy=False)
                    mail_notify.send_mail(stockName=stock, buy=False)
            except Exception as e:
                print("error aagyi yaar :-( Shayad aaj market band hai ", e)
        for stock in toBePurchasedStocksList:
            api_url = "https://www.alphavantage.co/query?function=MACD&symbol=" + stock + "&interval=daily&series_type=open&apikey=X51X1JMMQJUWY4SZ"
            response = requests.get(api_url)
            print(response)
            today = date.today()
            d1 = "20" + today.strftime("%y-%m-%d")
            try:
                latest_values = response.json()['Technical Analysis: MACD']['2021-08-20']
                print(latest_values)
                if latest_values['MACD'] >= latest_values['MACD_Signal']:
                    whatsapp_notify.send_message(stockName=stock, buy=True)
                    mail_notify.send_mail(stockName=stock, buy=True)
            except Exception as e:
                print("error aagyi yaar :-( Shayad aaj market band hai ", e)
        global breakit
        if breakit:
            sys.exit()
        time.sleep(3600)
def stop():
    global breakit
    breakit = True