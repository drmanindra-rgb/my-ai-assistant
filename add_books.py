 langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Put the exact name of your PDF book here!
book_file_name = "Bridwell.pdf" 

print(f"Reading {book_file_name}...")
try:
    loader = PyPDFLoader(book_file_name)
    pages = loader.load()
    
    # 2. Break the massive book into smaller 1000-letter chunks
    # We overlap them slightly so sentences don't get cut in half!
    print("Splitting the book into smaller pages for the AI...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    book_chunks = text_splitter.split_documents(pages)
    
    # 3. Save it to our existing digital filing cabinet
    print("Filing the book into the database. This might take a minute for a big book...")
    Chroma.from_documents(
        documents=book_chunks, 
        embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"), 
        persist_directory="./my_papers_db"
    )
    
    print("Success! Your spine book has been memorized by the AI!")
except Exception as e:
    print(f"Error: I couldn't load the file '{book_file_name}'. Make sure it is in your folder and spelled correctly!")
    print(f"(Computer details: {e})")