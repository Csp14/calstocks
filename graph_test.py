import matplotlib.pyplot as plt
import yfinance as yf
import mplfinance as mpf
import datetime as dt
import mpld3

def graph(ticker_symbol):
    start = dt.datetime(2024, 1, 1)
    end = dt.datetime.now()

    data = yf.download(ticker_symbol, start=start, end=end)
    colors = mpf.make_marketcolors(up="#00ff00", down="#ff0000", wick="inherit", edge="inherit", volume="in")
    mpf_style = mpf.make_mpf_style(base_mpf_style="nightclouds", marketcolors=colors)

    # Generate the plot directly using mpf.plot
    fig, ax = mpf.plot(data, type="candle", style=mpf_style, returnfig=True)

    # Convert the plot to HTML
    chart_html = mpld3.fig_to_html(fig)

    return chart_html


print(mpf.available_styles())