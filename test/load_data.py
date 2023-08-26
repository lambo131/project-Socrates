import streamlit as st
from langchain.document_loaders import WebBaseLoader
# PDF load module
from langchain.text_splitter import RecursiveCharacterTextSplitter

option = st.selectbox(
    'Choose document source',
    ('web address', 'upload file(pdf)', 'text input'))

if option == "web address":
    web_address = st.text_input("web address")
    
if option == "upload file(pdf)":
    uploaded_file = st.file_uploader("Choose a file")

if option == "text input":
    st.text_input("text input")

if load_text_button = st.button("load text"):
    