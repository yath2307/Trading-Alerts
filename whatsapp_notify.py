from twilio.rest import Client
from cryptography.fernet import Fernet

key = key = b'AOf70Pp9VfoOUkOux2YN8U_c5Ute9KOXFWQH5ywrPss='
token = b'gAAAAABhNPa3bsmYIcYqTWsx1txi3OvitimCrL28z_Gugy9SmmjsH2FcAzzVV9yvgpFlkXFAFD_xiTSeejjLdPicVgbC9MhdXTkv2MVahHR1Fm-0NisiT3Ec1fCn8tv58bk4ZLwaaceQ'
fernet = Fernet(key)
sid = b'gAAAAABhNPeGycWtNVfJmyAybxSP8kWPXcwtXc0uItCYo-fxvmy5IUAb1pkCpYpZRn202aW8Ojzvk6hl5U09u2uHohD9Rp8tW802u_cmtbJDISLaeaOjZmnNW1ojZdiESJhOwvgeNZ7J'

def send_message(stockName, buy, reco=None):
    account_sid = fernet.decrypt(sid).decode()
    auth_token = fernet.decrypt(token).decode()
    client = Client(account_sid, auth_token)
    if buy is True and reco is not None:
        body = "Buy signal for stock " + stockName + " according to MACD crossings " + "TickerTape buy recommendation : Total Reco: " + str(
            reco["totalReco"]) + " percentage buy reco: " + str(reco["percBuyReco"])
    elif buy is True and reco is None:
        body = "Buy signal for stock " + stockName + " according to MACD crossings "
    else:
        body = "Sell signal for stock " + stockName + " according to MACD crossings"

    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body=body,
        to="whatsapp:+918630019767"
    )

    print(message.sid)
