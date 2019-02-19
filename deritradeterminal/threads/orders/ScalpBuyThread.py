from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager


class ScalpBuyThread(QThread):

    signeler = pyqtSignal(bool,str,str) 

    def processOrder(self):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[self.accountid][0], config.tradeApis[self.accountid][1], ConfigManager.get_config().apiUrl)
            client.buy(ConfigManager.get_config().tradeInsturment, float(self.amount), 0, "market")

            self.signeler.emit(True, "Market Buy Order Success", "Market Buy On Account: " + str(self.accountid) + " For Amount: " + str(self.amount))

        except Exception as e:
            self.signeler.emit(False, "Scalp Buy Order Error", "Failed to scalp buy on " + str(self.accountid) + " for amount: " + str(self.amount) + "\n" + str(e))

        if position['direction'] == "buy":

                try:

                    self.amount = float(self.scalpAmountInput.text()) * float(self.scalpTPInput.text()) / 100
                    self.price =  round(position["averagePrice"] * (1.0 + float(self.scalpTPInput.text()) / 100), 8)
                    print("Trying to send sell limit order at " + str(price) + " near " + str(position["averagePrice"]))
                    client = RestClient(config.tradeApis[self.accountid][0], config.tradeApis[self.accountid][1],ConfigManager.get_config().apiUrl)
                    client.sell(ConfigManager.get_config().tradeInsturment, amount, price, "limit")

    def __init__(self, accountid, price, amount, position):
        QThread.__init__(self)
        self.accountid = accountid
        self.price = price
        self.amount = amount
        self.position = position

    def run(self):
        self.processOrder()
