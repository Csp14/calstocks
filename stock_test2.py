import yfinance as yf
import pprint
stock = yf.Ticker("NVDA")

quarterly = []

price = stock.history(period="5d")
print(price)
print(price.iloc[2][2])

info = stock.info
pprint.pprint(info)