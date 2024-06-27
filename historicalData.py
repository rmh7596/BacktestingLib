from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import Contract
import time
import requests
import json

class TradeApp(EWrapper, EClient): 
    def __init__(self): 
        EClient.__init__(self, self)
        self.nextValidOrderId = None
        self.permId2ord = {}
        self.cashbalance = 0

    @iswrapper
    def nextValidId(self, orderId:int):
        super().nextValidId(orderId)
        logging.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId

    def EurUsdFx(self):
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "USD"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract
    
    def USStock(self, sym):
        #! [stkcontract]
        contract = Contract()
        contract.symbol = sym
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        contract.primaryExchange = "ARCA"
        #! [stkcontract]
        return contract
    
    def etf(self, sym):
        contract = Contract()
        contract.symbol = sym
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract
    
    def USOptionContract(self, sym, right, strike, expiration):
        #! [optcontract_us]
        contract = Contract()
        contract.symbol = sym
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = expiration #"20190315"
        contract.strike = strike #1180
        contract.right = right #"C"
        contract.multiplier = "100"
        #! [optcontract_us]
        return contract    

    def headTimestamp(self, reqId, headTimestamp):
        print(reqId, headTimestamp)
    
    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        tick_type = TickTypeEnum.to_str(tickType)
        if tick_type == "BID":
            self.bid = price
            print("self.bid", self.bid)
        if tick_type == "ASK":
            self.ask = price
            print("self.ask", self.ask)
    
    def historicalData(self, reqId, bar):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)

    def historicalSchedule(self, reqId: int, startDateTime: str, endDateTime: str, timeZone: str, sessions: ListOfHistoricalSessions):
        print("HistoricalSchedule. ReqId:", reqId, "Start:", startDateTime, "End:", endDateTime, "TimeZone:", timeZone)
        for session in sessions:
            print("\tSession. Start:", session.startDateTime, "End:", session.endDateTime, "Ref Date:", session.refDate)
    
    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate. ReqId:", reqId, "BarData.", bar)
    
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)

# For historical data
#app.reqHeadTimeStamp(1, app.EurUsdFx(), "BID_ASK", 1, 1)

def get_stock_history(app: TradeApp, stock):
    #app.reqMarketDataType(1)
    #app.reqMktData(1, app.USStock(stock), "", True, False, []) # Only want one snapshot price
    app.reqHistoricalData(reqId=101, 
                          contract=app.USStock(stock),
                          endDateTime='', # up until the current moment
                          durationStr='1 D',
                          barSizeSetting='1 hour',
                          whatToShow='Trades',
                          useRTH=0,                 #0 = Includes data outside of RTH | 1 = RTH data only 
                          formatDate=1,    
                          keepUpToDate=0,           #0 = False | 1 = True 
                          chartOptions=[])


def main():
    # things
    app = TradeApp()
    app.connect("127.0.0.1", 4001, clientId=0)
    time.sleep(1)
    # Function for what we wanna do
    get_stock_history(app, "TSLA")
    time.sleep(1)
    app.run()

if __name__ == "__main__":
    main()