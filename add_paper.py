import os

# Step A: NO MORE API KEY! 
# We are using a free open-source AI now, so we don't need passwords or money.

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

print("Opening the filing cabinet...")

# Step B: Let's create a fake mini-research paper to test it out!
my_science_paper = """
Title: The Future of AI in 2026
Research shows that artificial intelligence is now being used to analyze stock markets 
and read complex documents. The most popular language for building AI is Python.
"""

# Turn our text into a 'Document' file folder that the AI can understand
doc = Document(page_content=my_science_paper)

# Step C: Put the folder inside our Chroma database using the free AI
# This will download a small, free AI model to your computer the first time you run it!
Chroma.from_documents(
    documents=[doc], 
    embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"), 
    persist_directory="./my_papers_db"
)

print("Success! Your research paper has been filed away. The AI can now read it!")