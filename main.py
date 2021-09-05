
from flask import Flask
import fetching_data
app = Flask(__name__)

@app.route('/start')
def startTracking():
    fetching_data.start()
    return 'started tracking stocks'

@app.route('/stop')
def stopTracking():
    fetching_data.stop()
    return 'stopped tracking stocks'

# @app.route('/get/purchased')
# def getPurchased():
#     return ' '.join([str(elem) for elem in fetching_data.purchasedStocksList])
#
# @app.route('/get/toBePurchased')
# def getToBePurchased():
#     return ' '.join([str(elem) for elem in fetching_data.toBePurchasedStocksList])
#
# @app.route('/add/toBePurchased/<symbol>')
# def addToBePurchasedStocks(symbol):
#     fetching_data.toBePurchasedStocksList.append(symbol)
#     return 'Added Stock '+symbol+' to the list '
#
# @app.route('/remove/toBePurchased/<symbol>')
# def removeToBePurchasedStocks(symbol):
#     fetching_data.toBePurchasedStocksList.remove(symbol)
#     return 'Removed Stock '+symbol+' from the list '
#
#
# @app.route('/add/purchased/<symbol>')
# def addPurchasedStocks(symbol):
#     fetching_data.purchasedStocksList.append(symbol)
#     return 'Added Stock '+symbol+' to the list '
#
# @app.route('/remove/purchased/<symbol>')
# def removePurchasedStocks(symbol):
#     fetching_data.purchasedStocksList.append(symbol)
#     return 'Removed Stock '+symbol+' from the list '

if __name__ == '__main__':
     app.run(port='5002')