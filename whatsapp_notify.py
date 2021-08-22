from twilio.rest import Client

def send_message(stockName,buy):
    account_sid = 'AC51d373f200999f320cfd35b123b73c97'
    auth_token = '0b6642e037beea7ba8058335740a50cd'
    client = Client(account_sid, auth_token)
    if buy==True:
        body='Buy signal for stock '+stockName+' according to MACD crossings'
    else:
        body='Sell signal for stock '+stockName+' according to MACD crossings'

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=body,
        to='whatsapp:+918630019767'
    )

    print(message.sid)