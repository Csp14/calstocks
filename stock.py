import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator
import time

def calculate_ema(data, span):
    indicator_ema = EMAIndicator(close=data['Close'], window=span, fillna=True)
    return indicator_ema.ema_indicator()

def generate_signals(data):
    # Calculate EMAs
    data['ema_5'] = calculate_ema(data, 5)
    data['ema_10'] = calculate_ema(data, 10)
    data['ema_20'] = calculate_ema(data, 20)
    
    # Generate buy/sell signals based on strategy
    conditions = (
        (data['ema_5'] > data['ema_10']) &
        (data['ema_5'] > data['ema_20']) &
        (data['ema_10'] > data['ema_20'])
    )
    
    data['signal'] = conditions.map({True: 'BUY', False: 'SELL'})
    
    # Return the signal for the most recent date
    return data['signal'].iloc[-1]
while (True):

    def main():
        # Input the stock ticker symbol
        ticker_symbol = input("Enter stock ticker symbol: ")
        
        # Fetch historical data using yfinance
        data = yf.download(ticker_symbol, period="1y")
        
        # Drop rows with missing values
        data.dropna(inplace=True)
        
        # Generate buy/sell signals
        signal = generate_signals(data)
        
        # Display the signal
        print(f"Signal for {ticker_symbol}: {signal}")
        
        # Print out the calculated EMAs
        print("Exponential Moving Averages (EMAs):")
        print(f"EMA 5-day: {data['ema_5'].iloc[-1]}")
        print(f"EMA 10-day: {data['ema_10'].iloc[-1]}")
        print(f"EMA 20-day: {data['ema_20'].iloc[-1]}")
    time.sleep(2)

    if __name__ == "__main__":
        main()
