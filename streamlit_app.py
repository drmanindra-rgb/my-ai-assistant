import os
os.environ["GOOGLE_API_KEY"] = "GOOGLE_API_KEY"
import streamlit as st
from assistant import boss_ai # Import the massively upgraded function!

st.title("🌟 My Autonomous AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything... I have a real brain now!"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # You no longer need if/elif statements here. The LLM handles everything!
    response = boss_ai(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})