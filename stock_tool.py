import yfinance as yf

def check_stock_price(ticker_symbol):
    """This function goes to the internet and gets real stock numbers."""
    try:
        # If someone says 'Apple', the ticker is 'AAPL'
        stock = yf.Ticker(ticker_symbol)
        today_data = stock.history(period="1d")
        
        # Grab the latest price
        current_price = today_data['Close'].iloc[-1]
        return f"The current price of {ticker_symbol} is ${current_price:.2f}"
    except Exception:
        return "Sorry, I couldn't find that stock symbol."