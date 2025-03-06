import streamlit as st
import os
import requests
import logging
import numpy as np
import pandas as pd
from io import BytesIO
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from google import generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

#################################################################
# Logging Setup
#################################################################
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Application startup.")

#################################################################
# Load Environment Variables and Configure Google Generative AI
#################################################################
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY is missing in .env file.")
    logging.error("Missing GOOGLE_API_KEY in .env")
    st.stop()
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing in .env file.")
    logging.error("Missing GROQ_API_KEY in .env")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
logging.info("Google Generative AI configured.")

#################################################################
# Caching Document Processing with PyPDF2, pandas, and TXT
#################################################################
@st.cache_data(show_spinner=False)
def cached_process_documents(file_data):
    logging.info("Processing documents via cache.")
    full_text = ""
    for name, content in file_data:
        if name.endswith(".pdf"):
            try:
                pdf_reader = PdfReader(BytesIO(content))
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
                logging.info(f"Processed PDF: {name}")
            except Exception as e:
                logging.error(f"Error processing PDF {name}: {e}")
        elif name.endswith(".csv"):
            try:
                df = pd.read_csv(BytesIO(content))
                full_text += df.astype(str).apply(lambda x: " ".join(x), axis=1).str.cat(sep="\n") + "\n"
                logging.info(f"Processed CSV: {name}")
            except Exception as e:
                logging.error(f"Error processing CSV {name}: {e}")
        elif name.endswith(".txt"):
            try:
                full_text += content.decode("utf-8") + "\n"
                logging.info(f"Processed TXT: {name}")
            except Exception as e:
                logging.error(f"Error processing TXT {name}: {e}")
        else:
            logging.warning(f"Unsupported file type: {name}")
    return full_text

def process_documents(files):
    file_data = []
    for uploaded_file in files:
        try:
            file_content = uploaded_file.getvalue()
            file_data.append((uploaded_file.name.lower(), file_content))
        except Exception as e:
            logging.error(f"Error reading file {uploaded_file.name}: {e}")
    return cached_process_documents(file_data)

#################################################################
# Define LLM Classes
#################################################################
class GeminiLLM:
    def generate_response(self, prompt):
        logging.info("Generating response using Gemini.")
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # calling my model
        response = model.generate_content([prompt])
        
        return response.text

class GroqLLM:
    def __init__(self, model_name, api_key):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"
    
    def generate_response(self, prompt):
        logging.info("Generating response using GroqLLM.")
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200,
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            logging.error(f"Groq error: {response.status_code} {response.text}")
            return f"Error: {response.status_code} {response.text}"

#################################################################
# Sidebar Options for Model and Persona Selection
#################################################################
model_choice = st.sidebar.selectbox("Select Model", ["Gemini", "Groq"])
persona_style = st.sidebar.selectbox("Select Persona Style", ["Formal", "Professional", "Casual"])

if model_choice == "Gemini":
    llm = GeminiLLM()
elif model_choice == "Groq":
    llm = GroqLLM("llama-3.3-70b-versatile", GROQ_API_KEY)

def apply_persona(prompt, persona):
    if persona == "Formal":
        return f"Please respond in a formal tone. {prompt}"
    elif persona == "Professional":
        return f"Please answer in a professional manner. {prompt}"
    elif persona == "Casual":
        return f"Answer casually: {prompt}"
    return prompt

def add_document_context(prompt):
    doc_context = st.session_state.get("document_context", "")
    if doc_context.strip():
        return f"{prompt}\n\nDocument Context:\n{doc_context}"
    return prompt

#################################################################
# Multi-Turn Dialogue: Maintain Conversation Context
#################################################################
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "document_context" not in st.session_state:
    st.session_state.document_context = ""

def add_to_history(role, message):
    st.session_state.chat_history.append({"role": role, "content": message})
    logging.info(f"Added to history: {role} - {message}")

def get_history_text():
    return "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in st.session_state.chat_history])

#################################################################
# Optional: Conversational QA Chain for Document QA
#################################################################
def get_conversational_chain():
    prompt_template = """
Answer the question in as much detail as possible from the provided context.
If the answer is not found in the provided context, reply: "Answer is not available in the documents."
Context:
{context}
Question:
{question}
Answer:
"""
    model_chain = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model_chain, chain_type="stuff", prompt=prompt)
    return chain

def process_query_with_docs(user_question):
    if st.session_state.document_context:
        chain = get_conversational_chain()
        response = chain({"input_documents": [st.session_state.document_context], "question": user_question}, return_only_outputs=True)
        return response["output_text"]
    else:
        return "No document context available."

#################################################################
# Main App: Navigation and Functionalities
#################################################################
st.title("Arogo AI Assistant with Groq API Integration")

# Sidebar: File uploader for documents (PDF, CSV, TXT)
uploaded_files = st.sidebar.file_uploader(
    "Upload your PDF, CSV, or TXT documents",
    accept_multiple_files=True,
    type=["pdf", "csv", "txt"]
)
if st.sidebar.button("Process Documents"):
    if uploaded_files:
        with st.spinner("Processing documents..."):
            doc_text = process_documents(uploaded_files)
            st.session_state.document_context = doc_text
            logging.info("Documents processed and context saved.")
        st.success("Documents processed and context saved.")
    else:
        st.warning("Please upload at least one file.")

# Sidebar: Functionality selection
functionality = st.sidebar.selectbox("Choose Functionality", [
    "Home", "Summarization", "Sentiment Analysis", "NER", "Question Answering", "Code Generation", "Multi-Turn Dialogue & Document QA"
])

#################################################################
# Standard NLP Functionalities (with optional Document Context)
#################################################################
if functionality == "Home":
    st.write("Welcome to the Arogo AI Streamlit App. Use the sidebar to select a functionality.")

elif functionality == "Summarization":
    text_input = st.text_area("Enter text for Summarization:")
    if st.button("Summarize"):
        base_prompt = f"Summarize the following text concisely:\n{text_input}"
        prompt = add_document_context(apply_persona(base_prompt, persona_style))
        summary = llm.generate_response(prompt)
        logging.info("Summarization performed.")
        st.write("Summary:", summary)
        
elif functionality == "Sentiment Analysis":
    text_input = st.text_area("Enter text for Sentiment Analysis:")
    if st.button("Analyze Sentiment"):
        base_prompt = f"Analyze the sentiment of the following text as positive, negative, or neutral:\n{text_input}"
        prompt = add_document_context(apply_persona(base_prompt, persona_style))
        sentiment = llm.generate_response(prompt)
        logging.info("Sentiment analysis performed.")
        st.write("Sentiment:", sentiment)
        
elif functionality == "NER":
    text_input = st.text_area("Enter text for Named Entity Recognition:")
    if st.button("Extract Entities"):
        base_prompt = f"Extract and list the names, locations, and dates mentioned in the text:\n{text_input}"
        prompt = add_document_context(apply_persona(base_prompt, persona_style))
        entities = llm.generate_response(prompt)
        logging.info("NER performed.")
        st.write("Entities:", entities)
        
elif functionality == "Question Answering":
    context = st.text_area("Enter Context:")
    question = st.text_input("Enter your Question:")
    if st.button("Get Answer"):
        base_prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        prompt = add_document_context(apply_persona(base_prompt, persona_style))
        answer = llm.generate_response(prompt)
        logging.info("Question Answering performed.")
        st.write("Answer:", answer)
        
elif functionality == "Code Generation":
    code_description = st.text_area("Enter description for code generation:")
    language = st.selectbox("Select Language", ["Python", "JavaScript", "Java", "C++", "Other"])
    lang_map = {
        "Python": "python",
        "JavaScript": "javascript",
        "Java": "java",
        "C++": "cpp",
        "Other": "plaintext"
    }
    if st.button("Generate Code"):
        base_prompt = f"Generate {language} code for the following problem:\n{code_description}"
        prompt = add_document_context(apply_persona(base_prompt, persona_style))
        generated_code = llm.generate_response(prompt)
        logging.info("Code Generation performed.")
        st.code(generated_code, language=lang_map.get(language, "plaintext"))

#################################################################
# Multi-Turn Dialogue & Document QA (using processed document context)
#################################################################
elif functionality == "Multi-Turn Dialogue & Document QA":
    st.subheader("Multi-Turn Dialogue")
    history_text = get_history_text()
    if history_text:
        st.text_area("Conversation History", history_text, height=150, disabled=True)
    
    user_message = st.text_input("Your Message:", key="user_message")
    if st.button("Send"):
        add_to_history("user", user_message)
        dialogue_context = get_history_text()
        doc_context = st.session_state.document_context if st.session_state.document_context.strip() else ""
        full_prompt = f"{dialogue_context}"
        if doc_context:
            full_prompt += f"\n\nDocument Context:\n{doc_context}"
        full_prompt += "\n\nRespond to the conversation above."
        final_prompt = apply_persona(full_prompt, persona_style)
        response = llm.generate_response(final_prompt)
        add_to_history("assistant", response)
        logging.info("Multi-turn dialogue message sent.")
        st.text_area("Updated Conversation", get_history_text(), height=150, disabled=True)
    
    st.markdown("### Document QA")
    user_question = st.text_input("Ask a question about the uploaded documents:")
    if st.button("Get Document Answer"):
        doc_answer = process_query_with_docs(user_question)
        logging.info("Document QA performed.")
        st.write("Document Answer:", doc_answer)

logging.info("Application operations completed for this session.")
