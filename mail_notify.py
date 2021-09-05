import smtplib, ssl

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "yatharthguptaversion2@gmail.com"
password = "Gupt@15168360"

def send_mail(stockName, buy, reco=None):
    if buy is True and reco is not None:
        body = "Buy signal for stock "+stockName+" according to MACD crossings "+"TickerTape buy recommendation "+"TickerTape buy recommendation : Total Reco: "+str(reco["totalReco"])+" percentage buy reco: "+str(reco["percBuyReco"])
    elif buy is True and reco is None:
        body = "Buy signal for stock " + stockName + " according to MACD crossings "
    else:
        body = "Sell signal for stock "+stockName+" according to MACD crossings"
    # Create a secure SSL context
    context = ssl.create_default_context()
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail("yatharthguptaversion2@gmail.com", "yatharthgupta230799@gmail.com", body)
    except Exception as e:
        print("error aagyi yaar :-( "+e)
    finally:
        server.quit()
