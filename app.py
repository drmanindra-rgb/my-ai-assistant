import chainlit as cl
from stock_tool import check_stock_price
from reading_tool import search_my_papers
import os
from google.generativeai import configure, GenerativeModel

# Configure Gemini with your Google API Key
configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def get_google_search_results(query):
    """Uses Google Search grounding to fetch real-time information."""
    model = GenerativeModel("gemini-1.5-flash")
    # Using tools=google_search_retrieval allows the AI to search the web
    response = model.generate_content(
        query,
        tools=[{"google_search_retrieval": {}}]
    )
    return response.text

def boss_ai(user_prompt):
    text = user_prompt.lower()
    
    # 1. If asking about Nifty or a Stock, use the live price checker
    if "nifty" in text or "stock" in text or "price" in text:
        ticker = "^NSEI" if "nifty" in text else "AAPL"
        price_info = check_stock_price(ticker)
        
        if "error" in price_info.lower() or "not found" in price_info.lower():
            return f"I couldn't get the live price, but here is the latest search on {ticker}: \n\n{get_google_search_results(ticker)}"
        return price_info
        
    # 2. If asking about Research, use the filing cabinet
    elif "research" in text or "paper" in text or "ai" in text:
        db_results = search_my_papers(user_prompt)
        
        if "not found" in db_results.lower() or len(db_results) < 50:
            return f"Searching Google for: {user_prompt}\n\n{get_google_search_results(user_prompt)}"
        return db_results
        
    # 3. Fallback to a general Google Search
    else:
        return get_google_search_results(user_prompt)