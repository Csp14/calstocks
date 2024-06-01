import yfinance as yf
import pprint
import matplotlib
import numpy
import pandas as pd
msft = yf.Ticker("MSFT")
infor = msft.info

live_price = msft.history(period='1d')['Close'].iloc[-1]


high_price = infor["targetHighPrice"]
low_price = infor["targetLowPrice"]
news = msft.news
news_list = []

for piece in news:
    news_list.append(piece)

print("Target High Price: "+str(high_price))
print("Target Low Price: "+str(low_price))
print("Live Price: "+str(live_price))


percentage_high_target = ((high_price-live_price)/live_price)*100
percentage_low_target = ((low_price-live_price)/live_price)*100

print(len(news_list))
print(news_list[0]["title"])



#if percentage_high_target>0:
    #print("Stock is under analyst expectations")
#else:
    #print("Stock is over current price target")
#print("{:.2f}".format(percentage_high_target)+"%")

#if percentage_low_target>0:
    #print("price is currently under the earnings expecations even for low target")
#else:
    #print("low expecation target is below current stock price")
#print("{:.2f}".format(percentage_low_target)+"%")

#if percentage_low_target>0 and percentage_high_target>0:
    #print("For both low target and high targets, the stock is below the targets. The expected return ranges from ", percentage_low_target, percentage_high_target)

