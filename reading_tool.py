import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

def search_my_papers(question):
    # 1. Open the filing cabinet
    filing_cabinet = Chroma(
        persist_directory="./my_papers_db", 
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )
    
    # 2. Get the raw matching text
    matching_secrets = filing_cabinet.similarity_search(question, k=3)
    
    # 🚨 DIAGNOSTIC: Print exactly what the cabinet found
    print(f"\n--- 📂 CABINET OPENED: Found {len(matching_secrets)} matching chunks ---")
    for idx, doc in enumerate(matching_secrets):
        print(f"📄 Match {idx+1} Tags: {doc.metadata}")
    print("----------------------------------------------------------------\n")

    found_text = "\n".join([doc.page_content for doc in matching_secrets])
    
    if not found_text.strip():
        return "I couldn't find the answer in your local files."
    
    # 3. Use the Google Gemini Brain with STRICT NEW RULES
    try:
        # LEVEL 1: The Zero-Creativity Switch (temperature=0)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
        
        # LEVEL 2: The "Show Your Work" Guardrail (Strict Prompting)
        draft_prompt = f'''You are a professional medical AI Assistant. 
        Read the following notes retrieved from my private filing cabinet:
        
        {found_text}
        
        Question: {question}
        
        Strict Rules:
        1. Answer the question using ONLY the notes provided above.
        2. You MUST include at least one direct quote from the notes, wrapped in "quotation marks", to prove your answer.
        3. If you cannot find a direct quote that answers the question, you must reply EXACTLY with: "I couldn't find the answer in your local files."
        '''
        
        # Draft the initial answer
        draft_response = llm.invoke(draft_prompt)
        draft_answer = draft_response.content
        
        # LEVEL 3: The Internal Reviewer (Self-Correction Loop)
        review_prompt = f'''
        Original Notes: {found_text}
        
        AI Draft Answer: {draft_answer}
        
        Task: Did the AI Draft Answer include ANY information, facts, or claims that are NOT explicitly stated in the Original Notes? 
        Did it fail to include a direct quote from the notes?
        
        Reply ONLY with 'PASS' if the answer is 100% accurate to the notes AND contains a direct quote. 
        Reply ONLY with 'FAIL' if it hallucinated, made up facts, or forgot the quote.
        '''
        
        # The AI grades its own draft
        grade = llm.invoke(review_prompt).content
        
        if "FAIL" in grade.upper():
            print("🤖 Boss AI Reviewer: I caught a hallucination in the draft! Recalculating...")
            # If it failed, it tries one more time with a stricter warning
            strict_retry_prompt = draft_prompt + "\n\nWARNING: Your previous attempt failed the review. Stick STRICTLY to the text and include a quote."
            retry_response = llm.invoke(strict_retry_prompt)
            return retry_response.content
        else:
            print("🤖 Boss AI Reviewer: Draft passed fact-check.")
            return draft_answer
            
    except Exception as e:
        return f"Error connecting to Google Brain: {e}"
