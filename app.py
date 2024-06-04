from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import yfinance as yf
from ta.trend import EMAIndicator
from create_plot import create_plot
from graph_test import graph
from admin_routes import *
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

admin_message = None
#login admin
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    return login()

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard_route():
    return admin_dashboard()

@app.route('/logout', methods=['GET', 'POST'])
def admin_logout():
    return logout()


@app.route('/admin/message', methods=['POST'])
def admin_message_route():
    global admin_message
    message = request.form['message']
    admin_message = message
    return redirect(url_for('admin_dashboard_route'))  


@app.route('/bored')
def bored():
    global admin_message
    if admin_message:
        message = admin_message
        admin_message = None  # Reset the admin message after displaying it once
    else:
        message = "No message from admin"
    return render_template('bored.html', message=message)





def get_company_info(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    ticker_symbol = ticker_symbol.upper()
    company_name = stock.info['longName']
    company_description = stock.info['longBusinessSummary']
    current_price = get_live_price(ticker_symbol)
    sector = stock.info['sector']
    industry = stock.info['industry']
    recommendation = stock.info['recommendationKey']

    return company_name, company_description, current_price, sector, industry, recommendation

def get_live_price(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    live_price = stock.history(period='1d')['Close'].iloc[-1]
    return live_price

def calculate_ema(data, span):
    indicator_ema = EMAIndicator(close=data['Close'], window=span, fillna=True)
    return indicator_ema.ema_indicator()

def generate_signals(data):
    data['ema_5'] = calculate_ema(data, 5)
    data['ema_10'] = calculate_ema(data, 10)
    data['ema_20'] = calculate_ema(data, 20)
    conditions = (
        (data['ema_5'] > data['ema_10']) &
        (data['ema_5'] > data['ema_20']) &
        (data['ema_10'] > data['ema_20'])
    )
    data['signal'] = conditions.map({True: 'BUY', False: 'SELL'})
    return data['signal'].iloc[-1]













@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker_symbol = request.form['ticker']
        data = yf.download(ticker_symbol, period="1y")
        data.dropna(inplace=True)
        signal = generate_signals(data)
        company_name, company_description, current_price, sector, industry, recommendation = get_company_info(ticker_symbol)
        ema_5 = data['ema_5'].iloc[-1]
        ema_10 = data['ema_10'].iloc[-1]
        ema_20 = data['ema_20'].iloc[-1]
        return render_template('index.html', ticker_symbol=ticker_symbol, signal=signal, ema_5=ema_5, ema_10=ema_10, ema_20=ema_20,
                               company_name=company_name, company_description=company_description, current_price=current_price, sector=sector,
                                recommendation = recommendation, industry=industry)
    return render_template('index.html')

@app.route('/liveprice/<ticker_symbol>')
def live_price(ticker_symbol):
    live_price = get_live_price(ticker_symbol)
    return jsonify({'live_price': float(live_price)})

@app.route('/financial_details/<ticker_symbol>')
def financial_details(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    income_statement = stock.income_stmt.to_html()
    quarterly_income_statement = stock.quarterly_income_stmt.to_html()
    balance_sheet = stock.balance_sheet.to_html()
    quarterly_balance_sheet = stock.quarterly_balance_sheet.to_html()
    cash_flow_statement = stock.cashflow.to_html()
    quarterly_cash_flow_statement = stock.quarterly_cashflow.to_html()
    
    return render_template('financial_details.html', ticker_symbol=ticker_symbol,
                           income_statement=income_statement, quarterly_income_statement=quarterly_income_statement,
                           balance_sheet=balance_sheet, quarterly_balance_sheet=quarterly_balance_sheet,
                           cash_flow_statement=cash_flow_statement, quarterly_cash_flow_statement=quarterly_cash_flow_statement)

@app.route('/holding_details/<ticker_symbol>')
def holding_details(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    major_holders = stock.major_holders
    institutional_holders = stock.institutional_holders
    mutualfund_holders = stock.mutualfund_holders
    insider_transactions = stock.insider_transactions
    insider_purchases = stock.insider_purchases
    insider_roster_holders = stock.insider_roster_holders

    # Print statements for debugging
    print(f"Major Holders: {major_holders}")
    print(f"Institutional Holders: {institutional_holders}")
    print(f"Mutual Fund Holders: {mutualfund_holders}")
    print(f"Insider Transactions: {insider_transactions}")
    print(f"Insider Purchases: {insider_purchases}")
    print(f"Insider Roster Holders: {insider_roster_holders}")

    return render_template('holding_details.html', ticker_symbol=ticker_symbol,
                           major_holders=major_holders, institutional_holders=institutional_holders,
                           mutualfund_holders=mutualfund_holders, insider_transactions=insider_transactions,
                           insider_purchases=insider_purchases, insider_roster_holders=insider_roster_holders)
    
@app.route('/recommendations/<ticker_symbol>')
def recommendations(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    recommendations_summary = stock.recommendations_summary.to_html()
    recommendations = stock.recommendations.to_html()
    upgrades_downgrades = stock.upgrades_downgrades.to_html()

    return render_template('recommendations.html', ticker_symbol=ticker_symbol,
                           recommendations_summary=recommendations_summary,
                           recommendations=recommendations, upgrades_downgrades=upgrades_downgrades)

@app.route('/pricing_details/<ticker_symbol>')
def pricing_details(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)

@app.route('/pricing_data/<ticker_symbol>')
def pricing_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    live_price = stock.history(period='1d')['Close'].iloc[-1]
    information = stock.info
    high_price = information["targetHighPrice"]
    low_price = information["targetLowPrice"]
    percentage_high_target = ((high_price-live_price)/live_price)*100
    percentage_low_target = ((low_price-live_price)/live_price)*100

    plot_html = create_plot(percentage_high_target, percentage_low_target)
    return render_template('pricing_data.html', ticker_symbol=ticker_symbol, live_price=live_price, high_price = high_price, low_price=low_price, percentage_high_target=percentage_high_target, percentage_low_target=percentage_low_target, plot_html=plot_html)



if __name__ == '__main__':
    app.run(debug=True)

