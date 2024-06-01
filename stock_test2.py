import yfinance as yf
stock = yf.Ticker("NVDA")

quarterly = []

price = stock.history(period="5d")
print(price)
print(price.iloc[2][2])