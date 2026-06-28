from stock_tool import check_stock_price
from reading_tool import search_my_papers

def boss_ai(user_prompt):
    # Convert text to lowercase to make it easy to read
    text = user_prompt.lower()
    
    # Decision Matrix: The Boss decides who handles the job
    if "stock" in text or "price" in text:
        print("🤖 Boss AI: Sending this task to the Stock Sensor...")
        # Simple trick: extract a word that looks like a ticker symbol
        words = user_prompt.split()
        ticker = words[-1].upper() 
        return check_stock_price(ticker)
        
    elif "research" in text or "paper" in text or "ai" in text:
        print("🤖 Boss AI: Opening the Research Filing Cabinet...")
        return search_my_papers(user_prompt)
        
    else:
        return "🤖 Boss AI: I'm not sure which tool to use. Try asking about a stock (e.g., 'stock price AAPL') or 'research'."

# --- The Chat Loop! ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🌟 Welcome to Your Personal AI Assistant! 🌟")
    print("Type 'quit' to exit.")
    print("="*50 + "\n")
    
    # This 'while' loop lets you chat forever until you type quit!
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            print("🤖 Boss AI: Goodbye!")
            break
            
        answer = boss_ai(user_input)
        print(f"\n{answer}\n")