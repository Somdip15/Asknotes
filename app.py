import streamlit as st
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI
import os, shutil

from dotenv import load_dotenv
load_dotenv()

# Front end
st.title("AskNotes.ai")

# File Uploader
pdfs = st.file_uploader(label="Upload PDF", accept_multiple_files=True, type='.pdf')

# Create new directory
newpath = 'D:\VSCodePrograms\AskNotes\Asknotes\DataFiles'
if not os.path.exists(newpath):
    os.makedirs(newpath)

# Copy PDFs to new directory
for pdf in pdfs:
    try:
        shutil.copy(src=os.path.abspath(pdf.name), dst=f'D:\VSCodePrograms\AskNotes\Asknotes\DataFiles\{pdf.name}')
    except:
        st.write(f'{pdf.name} not found')
        break
    
# Prompt
prompt = st.text_input("Enter your prompt")

if prompt:
    loader = PyPDFLoader(newpath)
    index = VectorstoreIndexCreator().from_loaders([loader]) #Vectorizing

    llm = ChatOpenAI(model='gpt-4', verbose=True, temperature=0.6)

    response = index.query(prompt)
    st.write(response)
    print(response)