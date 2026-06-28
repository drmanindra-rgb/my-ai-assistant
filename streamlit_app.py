import streamlit as st
from stock_tool import check_stock_price
from reading_tool import search_my_papers

st.title("🌟 My AI Assistant Dashboard")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me about stocks or research..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get bot response (using your existing logic)
    text = prompt.lower()
    if "stock" in text or "price" in text:
        words = prompt.split()
        ticker = words[-1].upper() 
        response = check_stock_price(ticker)
    
    # We added "spine" and "book" right here so the AI knows to check the cabinet!
    elif "research" in text or "paper" in text or "ai" in text or "spine" in text or "book" in text:
        response = search_my_papers(prompt)
        
    else:
        response = "🤖 Boss AI: Try asking about a stock, research, or the spine!"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})