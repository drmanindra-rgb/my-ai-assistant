from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

print("📚 Boss AI: Opening the Bridwell Spine PDF...")

# 1. Load the PDF
loader = PyPDFLoader("Bridwell.pdf")
pages = loader.load_and_split()

print(f"📖 Boss AI: Found {len(pages)} pages. Chopping them into bite-sized notes...")

# 2. Open the filing cabinet and save the notes
filing_cabinet = Chroma.from_documents(
    documents=pages, 
    embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
    persist_directory="./my_papers_db"
)

print("✅ Boss AI: Done! All notes are securely filed in my_papers_db.")