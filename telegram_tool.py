from telethon.sync import TelegramClient

# Paste your API ID and API HASH from my.telegram.org here!
# Note: api_id must be a number (no quotes around it), and api_hash must have quotes!
API_ID = 34612876  # Replace with your real API ID
API_HASH = "cbe1883832367aca35fcd8f043feb061" # Replace with your real API HASH

def get_latest_channel_news(channel_list=None):
    """Logs into Telegram and reads the latest messages from MULTIPLE channels."""
    if channel_list is None:
        # Add all your favorite channel usernames here!
        channel_list = ["telegram", "StockScansAlertsBot", "PKScreener", "moneycontrolcom", "share_market_news_livee"] 

    try:
        # This opens a connection to Telegram as YOU
        with TelegramClient('my_user_session', API_ID, API_HASH) as client:
            news_text = "📰 Latest Market Updates:\n\n"
            
            # Loop through every channel in your list one by one
            for channel in channel_list:
                news_text += f"--- 🔹 {channel.upper()} ---\n"
                try:
                    # Fetch the 2 most recent messages from this specific channel
                    messages = client.get_messages(channel, limit=2)
                    for msg in messages:
                        if msg.text:
                            news_text += f"- {msg.text}\n\n"
                except Exception as e:
                    news_text += f"[Error reading this channel: {e}]\n\n"
                    
            return news_text
            
    except Exception as e:
        return f"Error connecting to Telegram: {e}"

# --- ONE-TIME LOGIN TEST ---
# Run this file directly ONE TIME to log in. 
if __name__ == "__main__":
    print("Testing Telegram Login...")
    # You can test it right here by adding real channel usernames to this list!
    print(get_latest_channel_news(["telegram", "StockScansAlertsBot", "PKScreener", "moneycontrolcom", "share_market_news_livee"]))