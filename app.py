import streamlit as st
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI
import time

from dotenv import load_dotenv
load_dotenv()

# Front end
st.set_page_config(page_title="Asknotes.ai", layout="wide", page_icon=':pencil:', initial_sidebar_state="auto")
st.title(":pencilAskNotes.ai")

# File Uploader
pdf = st.file_uploader(label="Upload your PDF", type='.pdf')

if pdf:
    #Chat interface
    if "message" not in st.session_state: # Initialize chat history
        st.session_state["message"] = []

    with st.chat_message(name="ai"): # Intro message
        st.write("Hi! I'm AskNotes.ai. Ask me anything about the uploaded PDF!")

    for message in st.session_state.message: # Display msg from chat history
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Prompt
    prompt = st.text_input("Enter your prompt")
    if prompt:
        with st.chat_message("user"): # Displays user message
            st.markdown(prompt)
        st.session_state.message.append({"role": "user", "content": prompt}) # Adds to chat history