import streamlit as st
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI
import  time

from dotenv import load_dotenv
load_dotenv()

# Front end
st.set_page_config(page_title="Asknotes.ai", layout="wide", page_icon='📝', initial_sidebar_state="auto")
st.title("📝AskNotes.ai")

# File Uploader
pdf = st.file_uploader(label="Upload your PDF", type='.pdf')

if pdf:
    # Chat interface
    if "message" not in st.session_state: # Initialize chat history
        st.session_state["message"] = []
    
    with st.chat_message(name="ai"): # Intro message
        st.write("Hi! I'm AskNotes.ai. Ask me anything about the uploaded PDF!")

    for message in st.session_state.message: # Display msg from chat history
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Prompt
    prompt = st.chat_input("Enter your question:")
    if prompt:
        with st.chat_message("user"): # Displays user message
            st.markdown(prompt)
        st.session_state.message.append({"role": "user", "content": prompt}) # Adds to chat history

        # Progress Bar
        progress_text_list = ["Scanning PDF...", "Gathering info...", "Vectorizing gathered info...", "Preparing response..."]
        progress_bar = st.progress(value=0, text=progress_text_list[0])
        
        # AI Response
        with st.chat_message("ai"):

            loader = PyPDFLoader('D:\VSCodePrograms\AskNotes\Data\Bitcoin.pdf')
            index = VectorstoreIndexCreator().from_loaders([loader])
            llm = ChatOpenAI(model='gpt-4', verbose=True, temperature=0.6)
            response = index.query(question=prompt)

            for percent_complete in range(100): # Animating progress bar
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1, text=progress_text_list[percent_complete//25])
            time.sleep(0.5)
            progress_bar.empty()

            st.write(response) # Generated response
        st.session_state.message.append({"role": "assistant", "content": response}) # Adds to chat history
else:
    st.warning("Attatch a PDF to start chatting")