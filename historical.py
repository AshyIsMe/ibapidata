
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time
import pandas as pd

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
		self.bars = []

	def historicalData(self, reqId, bar):
		#print(f'Time: {bar.date} Close: {bar.close}')
		print(bar)
		self.bars.append(bar)

def run_loop():
	app.run()

app = IBapi()
app.connect('127.0.0.1', 7497, 123)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server

#Create contract object
eurusd_contract = Contract()
eurusd_contract.symbol = 'EUR'
eurusd_contract.secType = 'CASH'
eurusd_contract.exchange = 'IDEALPRO'
eurusd_contract.currency = 'USD'

#Request historical candles
#app.reqHistoricalData(1, eurusd_contract, '', '2 D', '1 hour', 'BID', 0, 2, False, [])
app.reqHistoricalData(1, eurusd_contract, '', '20 D', '1 hour', 'BID', 0, 2, False, [])

time.sleep(5) #sleep to allow enough time for data to be returned
print(f"len(app.bars): {len(app.bars)}")
data = [{'date':b.date,'open':b.open,'high':b.high,'low':b.low,'close':b.close,'volume':b.volume,'average':b.average} for b in app.bars]
df = pd.DataFrame(data)
print(df.describe())
print(df)
app.disconnect()
