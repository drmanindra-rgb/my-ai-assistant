from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def search_my_papers(question):
    """This function searches your private filing cabinet for answers."""
    # 1. Open our digital filing cabinet using the exact same FREE AI model
    filing_cabinet = Chroma(
        persist_directory="./my_papers_db", 
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )
    
    # 2. Look for the sentences that match your question best
    matching_secrets = filing_cabinet.similarity_search(question, k=2)
    
    if not matching_secrets:
        return "I couldn't find anything about that in your papers."
    
    # 3. Combine what we found into a note for the boss AI
    found_text = "\n".join([doc.page_content for doc in matching_secrets])
    return f"Here is what I found in your papers:\n{found_text}"