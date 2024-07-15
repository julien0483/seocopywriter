import json
import re
import PyPDF2
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
import altair as alt
from langchain_anthropic import ChatAnthropic
from docx import Document#exceptions
from io import BytesIO
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import fitz  
st.set_page_config(page_title="Seo copywriter", layout="wide", initial_sidebar_state="expanded")
from docx.shared import Pt
import os
st.markdown('<h1>SEO CONTENT WRITER</h1>', unsafe_allow_html=True)

def get_checkbox_states(pdf):
    checkbox_states = []
    pdf_reader = PyPDF2.PdfReader(pdf)
    fields = pdf_reader.get_fields()
    if fields:
        checkboxes = {k: v.get('/V', 'Off') for k, v in fields.items() if v.get('/FT') == '/Btn'}
        checkbox_states.append(checkboxes)
    return checkbox_states

def get_pdf_text(pdf):
    texts = []
    text = ""
    pdf_document = fitz.open(stream=pdf.read(), filetype="pdf")
    for page_num in range(2, pdf_document.page_count):  # Start from the third page (index 2)
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    # Remove placeholders (underscores)
    text = re.sub(r'_{2,}', '', text)
    #print(get_checkbox_states(pdf))
    return text


def get_page_text(pdf):
    pdf_reader = PdfReader(pdf)
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    return pdf_reader

def create_word_doc(texts):
    doc = Document()
    for i, text in enumerate(texts):
        # Add a bold title before each text
        title = doc.add_paragraph()
        run = title.add_run(f"Page {i + 1}")
        run.bold = True
        run.font.size = Pt(14)
        doc.add_paragraph(text)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def get_vectorstore(texts):
    if not texts:
        raise ValueError("No texts to process for vector store creation.")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=texts, embedding=embeddings)
    return vectorstore

def handle_userinput(user_question):
    if "vectorstore" not in st.session_state:
        st.write("Error: Vectorstore not found. Please upload and process the PDFs first.")
        return
    vectorstore = st.session_state.vectorstore
    system_prompt = (
        """You are an expert in creating SEO-optimized website content. Your task is to develop content for a client's website based 
        on the detailed information provided.
         The content must be structured to enhance the website’s visibility in search engine results, 
         attract the target audience, and align with the client's business goals.
        """
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    llm = ChatOpenAI(model="gpt-4")
    
    #llm = ChatAnthropic(model='claude-2.1')
    retriever = vectorstore.as_retriever()
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    response = rag_chain.invoke({"input":"""

    """ + user_question})
    

    # Parse the JSON response
    try:
        response = response['answer']
        return response

    except json.JSONDecodeError:
        st.write("Error: Invalid JSON response")
        return

def main():

    load_dotenv()

    st.subheader("Dynamic Structure")

    num_pages = st.number_input("Number of pages:", min_value=1, max_value=10, value=1, step=1)
    pdf_templates_folder = 'pdf_templates'
    options = [f for f in os.listdir(pdf_templates_folder) if f.endswith('.pdf')]
    page_details = []

    for i in range(num_pages):
        st.write(f"### Page {i+1}")
        text_input_1 = st.text_input(f"Titre {i+1}")
        text_input_2 = st.text_input(f"URL Concurrent {i+1}")
        dropdown = st.selectbox(f'Choisir le template de structure pour la page {i+1}', options)
        
        page_details.append({
            "page": i+1,
            "text_input_1": text_input_1,
            "text_input_2": text_input_2,
            "dropdown": dropdown
        })


    st.subheader("Cahier des charges")
    pdf_docs = st.file_uploader(
        "Upload le cahier des charges ", accept_multiple_files=False)
    st.subheader("Structure des pages")
      
    if st.button("process"):
        with st.spinner("Processing"):
            texts = get_pdf_text(pdf_docs)
            if not texts:
                st.write("No text extracted from PDFs.")
                return

            vectorstore = get_vectorstore(texts)
            st.session_state.vectorstore = vectorstore
            print("structures dyal zbi")
            output_contenu=[]
            for i in range(num_pages):
                selected_template = page_details[i]['dropdown']
                with open(os.path.join(pdf_templates_folder, selected_template), 'rb') as template_file:
                    structure_text = get_pdf_text(template_file)
                output_page=handle_userinput("Ecris SEO contenu pour la page suivant la structure suivante : " + structure_text)
                print(output_page)
                output_contenu.append(output_page)
            print(output_contenu)
        word_buffer = create_word_doc(output_contenu)
        st.download_button(label="Download Word Document",
                data=word_buffer,
                file_name="SEOCONTENT.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        
if __name__ == "__main__":
    main()