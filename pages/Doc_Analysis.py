import base64
import os
import time
from tempfile import NamedTemporaryFile
from streamlit_option_menu import option_menu
import streamlit as st
from dotenv import load_dotenv

# import google.generativeai as gen_ai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain import PromptTemplate
import os

load_dotenv()
# Load environment variables securely (replace with your preferred method)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", google_api_key=GOOGLE_API_KEY
)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.0-pro-latest",
    google_api_key=GOOGLE_API_KEY,
    convert_system_message_to_human=True,
)


def display_pdf(document):
    with open(document, "rb") as file:
        pdf_64 = base64.b64encode(file.read()).decode("utf-8")
        display = f'<iframe src="data:application/pdf;base64,{pdf_64}"style="overflow: hidden; width: 100%; height: 450px; border-radius: 35px;"></iframe>'
        st.markdown(display, unsafe_allow_html=True)


def process_pdf(doc_loader, prompt_template):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(doc_loader.read())
        temp_file_path = temp_file.name

    try:
        # Use the temporary file path with PyPDFLoader
        doc = PyPDFLoader(temp_file_path)
        pages = doc.load_and_split()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000, chunk_overlap=1000
        )
        context = "\n\n".join(str(p.page_content) for p in pages)
        if context == "":
            st.info("Context is empty")

        else:
            texts = text_splitter.split_text(context)
            vector_index = Chroma.from_texts(texts, embeddings).as_retriever(
                search_kwargs={"k": 4}
            )
            QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)
            qa_chain = RetrievalQA.from_chain_type(
                llm,
                retriever=vector_index,
                return_source_documents=True,
                chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
            )

            return qa_chain, context
    finally:
        # Ensure temporary file is deleted even if exceptions occur
        os.remove(temp_file_path)


def answer_question(qa_chain, question):
    if not question:
        return None
    response_placeholder = st.empty()
    with st.spinner("Looking for relevant context..."):
        response = qa_chain({"query": question})
        response_text = response["result"]

    # streaming effect
    for i in range(len(response_text)):
        time.sleep(0.010)
        response_placeholder.write(response_text[: i + 1] + "•")
    return response_text


st.set_page_config(
    page_title="Document Analysis",
    page_icon=":gemini:",
    layout="centered",
    initial_sidebar_state="collapsed",
)
# with st.sidebar:
#  st.markdown(
#      """
#      <style>
#      .sidebar{

#          color: black;
#      }
#      </style>
#      <div class="sidebar">
#      <h1 style="color: #ffcd42; text-align: center; font-family: 'Outfit', sans-serif;">RAG Gemini</h1>
#      </div>
#      """,
#      unsafe_allow_html=True,
#  )

SAMPLE_QUESTIONS = ["Summary", "Gist", "Layout","Pointers", "Simple Language", "Conclusion"]
custom_font_css = """
<style>
</style>

"""

header_html = """
    <style>
        .header {
        font-weight: 800;
        font-size: 50px;
        padding-bottom: 25px;
        padding-top: 0px;
        
        }
        .header:hover {
            letter-spacing: 1px;
            cursor: pointer;
            font-weight:900;
            transition: 0.2s;
            
        
        }
    </style>
    <h1 class="header">Document Analysis</h1>
"""

# Display HTML
st.markdown(header_html, unsafe_allow_html=True)

st.markdown(
    """
    <style>
	[data-testid="stDecoration"] {
		display: none;
	}
    </style>""",
    unsafe_allow_html=True,
)



template_1 = """
You are a helpful assistant that reviews legal documents and provides helpful answers to questions .
Use the following pieces of context to answer the task or question at the end. 
If you don't know the response, don't try to make up anything. 
If there is seemingly no context for the question, respond with a general according to the context provided.
At the end of the document give a brief source of the answer within the document.
Be as helpful as possible and provide detailed answers to the questions.
Try to keep  the answers relatively longer.
Keep a cheery tone overall and try to keep the answers as positive as possible.

{context}

Question: {question}

Helpful Answer:
"""
template_2 = """ 
You are a helpful assistant that reviews research papers and provides helpful answers to questions asked.
Use the following pieces of context to answer the task or question at the end. 
If you don't know the response, don't try to make up anything. 
If there is seemingly no context for the question, respond with a general according to the context provided.
At the end of the document give a brief source of the answer within the document.
Be as helpful as possible and provide detailed answers to the questions.
Try to keep  the answers relatively longer.
Keep a cheery tone overall and try to keep the answers as positive as possible.

{context}

Question: {question}

Helpful Answer:
"""
selected = option_menu(
    None,
    ["Documents", "Research Papers"],
    icons=["file-earmark-person", "file-text"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important"},
        "nav": {"padding-bottom": "0px"},
        "nav-item": {"font-weight": "200", "font-family": "'Outfit', monospace"},
        "nav-link": {"text-align": "left", "margin": "0px"},
        "nav-link-selected": {
            "font-family": "'Outfit', monospace",
            "font-weight": "200",
        },
    },
)

# selected = st.selectbox("", ["Job Profiles", "Resumes"])
if selected == "Documents":
    doc_loader = st.file_uploader("", type=["pdf"])

    if doc_loader:
        qa_chain, context = process_pdf(doc_loader, template_1)
        st.success("RAG Setup Successfully")
        question = st.text_input("Ask a Question")
        response = answer_question(qa_chain, question)

    else:
        st.info("Upload a document to start RAG")

elif selected == "Research Papers":
    doc_loader = st.file_uploader("", type=["pdf"])
    if doc_loader:
        qa_chain, context = process_pdf(doc_loader, template_2)
        st.success("RAG Setup Successfully")
        question = st.text_input("Ask a Question")
        response = answer_question(qa_chain, question)

    else:
        st.info("Upload a document to start RAG")
