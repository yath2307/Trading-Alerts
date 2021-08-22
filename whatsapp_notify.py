from twilio.rest import Client

def send_message(stockName,buy):
    account_sid = 'AC51d373f200999f320cfd35b123b73c97'
    auth_token = 'e4bcb7310d4209e1cdcde2b8bc65114d'
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