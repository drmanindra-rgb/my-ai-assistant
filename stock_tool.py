import chainlit as cl
from stock_tool import check_stock_price
from reading_tool import search_my_papers
from duckduckgo_search import DDGS

def get_live_news(query):
    """Fetches live news from the web if the database doesn't have the answer."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
        return "\n".join([r['body'] for r in results])

def boss_ai(user_prompt):
    text = user_prompt.lower()
    
    # 1. If asking about Nifty or a Stock, use the live price checker
    if "nifty" in text or "stock" in text or "price" in text:
        # Use ^NSEI as it is the standard ticker for Nifty 50
        ticker = "^NSEI" if "nifty" in text else "AAPL"
        price_info = check_stock_price(ticker)
        
        # If the price tool gives a generic response, fetch live context
        if "error" in price_info.lower() or "not found" in price_info.lower():
            return f"I couldn't get the live price, but here is the latest news on {ticker}: \n\n{get_live_news(ticker)}"
        return price_info
        
    # 2. If asking about Research, use the filing cabinet
    elif "research" in text or "paper" in text or "ai" in text:
        db_results = search_my_papers(user_prompt)
        
        # If the database returns nothing helpful, use the web search as a fallback
        if "not found" in db_results.lower() or len(db_results) < 50:
            return f"I didn't find much in your local research papers, but here is what the web says:\n\n{get_live_news(user_prompt)}"
        return db_results
        
    # 3. Fallback to a general response if it doesn't know
    else:
        return "🤖 Boss AI: I'm currently focused on spine research and market prices. Try asking 'What is the price of Nifty?' or search for 'spine research'."