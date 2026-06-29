import os
import time
import urllib.request
import xml.etree.ElementTree as ET
import schedule
import telebot 
import subprocess 
from dotenv import load_dotenv # NEW: The vault reader!
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# --- PUSH NOTIFICATION SETUP ---
load_dotenv() # Unlocks the .env file

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN") 
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")                
bot = telebot.TeleBot(TELEGRAM_TOKEN)
# -------------------------------

def learn_new_research():
    print("\n🤖 Night Shift AI: Waking up to look for new research!")
    url = 'http://export.arxiv.org/api/query?search_query=all:spine&sortBy=submittedDate&sortOrder=descending&max_results=3'
    
    try:
        response = urllib.request.urlopen(url).read()
        root = ET.fromstring(response)
        new_documents = []
        
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            
            # --- Smart Tags ---
            published = entry.find('{http://www.w3.org/2005/Atom}published').text
            author = entry.find('{http://www.w3.org/2005/Atom}author')
            author_name = author.find('{http://www.w3.org/2005/Atom}name').text if author is not None else "Unknown"
            
            content = f"Title: {title}\nSummary: {summary}"
            
            smart_metadata = {
                "source": "ArXiv Auto-Learner",
                "year": published[:4],
                "author": author_name,
                "topic": "spine" 
            }
            
            doc = Document(page_content=content, metadata=smart_metadata)
            new_documents.append(doc)
        
        if new_documents:
            print("🤖 Night Shift AI: Filing new papers into your database...")
            Chroma.from_documents(
                documents=new_documents, 
                embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"), 
                persist_directory="./my_papers_db"
            )
            print("🤖 Night Shift AI: Done! The Boss AI now knows about these papers.")
            
            # --- NEW: AUTO-UPLOAD TO GITHUB ---
            try:
                print("☁️ Night Shift AI: Uploading new brain cells to GitHub...")
                # Fix: When using shell=True, the command must be a single string, not a list!
                subprocess.run("git add my_papers_db/", check=True, shell=True)
                subprocess.run('git commit -m "Night Shift AI: Auto-learned new papers!"', check=True, shell=True)
                subprocess.run("git push", check=True, shell=True)
                print("✅ GitHub update complete! Your Streamlit app will now restart.")
            except Exception as e:
                print(f"⚠️ Could not sync to GitHub automatically. Make sure Git is installed: {e}")
            # -----------------------------------
            
            # --- PROACTIVE PUSH NOTIFICATION ---
            try:
                msg = f"🚨 Boss, I found {len(new_documents)} new spine papers while you were sleeping! They have been filed with Smart Tags."
                bot.send_message(MY_CHAT_ID, msg)
                print("📲 Push notification sent to your phone!")
            except Exception as e:
                print(f"⚠️ Could not send push notification: {e}")
            # ------------------------------------

        else:
            print("🤖 Night Shift AI: No new papers found today.")
            
    except Exception as e:
        print(f"🤖 Night Shift AI: Oops, hit an error reading the database: {e}")


learn_new_research()
schedule.every(12).hours.do(learn_new_research)

print("\n⏰ The Night Shift AI is now running in the background.")
while True:
    schedule.run_pending()
    time.sleep(60)