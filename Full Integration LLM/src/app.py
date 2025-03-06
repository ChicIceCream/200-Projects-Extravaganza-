import streamlit as st
import os
import requests
import numpy as np
import pandas as pd
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from google import generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

#################################################################
# Load Environment Variables and Configure Google Generative AI
#################################################################
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY is missing in .env file.")
    st.stop()
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing in .env file.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

#################################################################
# File Processing Functions (without embeddings)
#################################################################
def get_file_text(files):
    full_text = ""
    for uploaded_file in files:
        filename = uploaded_file.name.lower()
        if filename.endswith(".pdf"):
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        elif filename.endswith(".csv"):
            try:
                df = pd.read_csv(uploaded_file)
                full_text += df.astype(str).apply(lambda x: " ".join(x), axis=1).str.cat(sep="\n") + "\n"
            except Exception as e:
                st.error(f"Error processing CSV: {e}")
        elif filename.endswith(".txt"):
            try:
                full_text += uploaded_file.getvalue().decode("utf-8") + "\n"
            except Exception as e:
                st.error(f"Error processing TXT file: {e}")
        else:
            st.warning(f"Unsupported file type: {uploaded_file.name}")
    return full_text

def process_documents(files):
    return get_file_text(files)

#################################################################
# Define LLM Classes
#################################################################
class GeminiLLM:
    def generate_response(self, prompt):
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

def preprocess_text(text):
    return text.lower()

#################################################################
# Multi-Turn Dialogue: Maintain Conversation Context
#################################################################
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "document_context" not in st.session_state:
    st.session_state.document_context = ""

def add_to_history(role, message):
    st.session_state.chat_history.append({"role": role, "content": message})

def get_history_text():
    return "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in st.session_state.chat_history])

#################################################################
# Optional: Build a Conversational QA Chain for Document QA
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
        st.success("Documents processed and context saved.")
    else:
        st.warning("Please upload at least one file.")

# Sidebar: Functionality selection
functionality = st.sidebar.selectbox("Choose Functionality", [
    "Home", "Summarization", "Sentiment Analysis", "NER", "Question Answering", "Code Generation", "Multi-Turn Dialogue & Document QA"
])

#################################################################
# Standard NLP Functionalities
#################################################################
if functionality == "Home":
    st.write("Welcome to the Arogo AI Streamlit App. Use the sidebar to select a functionality.")

elif functionality == "Summarization":
    text_input = st.text_area("Enter text for Summarization:")
    if st.button("Summarize"):
        prompt = apply_persona(f"Summarize the following text concisely:\n{text_input}", persona_style)
        summary = llm.generate_response(prompt)
        st.write("Summary:", summary)
        
elif functionality == "Sentiment Analysis":
    text_input = st.text_area("Enter text for Sentiment Analysis:")
    if st.button("Analyze Sentiment"):
        prompt = apply_persona(f"Analyze the sentiment of the following text as positive, negative, or neutral:\n{text_input}", persona_style)
        sentiment = llm.generate_response(prompt)
        st.write("Sentiment:", sentiment)
        
elif functionality == "NER":
    text_input = st.text_area("Enter text for Named Entity Recognition:")
    if st.button("Extract Entities"):
        prompt = apply_persona(f"Extract and list the names, locations, and dates mentioned in the text:\n{text_input}", persona_style)
        entities = llm.generate_response(prompt)
        st.write("Entities:", entities)
        
elif functionality == "Question Answering":
    context = st.text_area("Enter Context:")
    question = st.text_input("Enter your Question:")
    if st.button("Get Answer"):
        prompt = apply_persona(f"Context: {context}\n\nQuestion: {question}\n\nAnswer:", persona_style)
        answer = llm.generate_response(prompt)
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
        prompt = apply_persona(f"Generate {language} code for the following problem:\n{code_description}", persona_style)
        generated_code = llm.generate_response(prompt)
        st.code(generated_code, language=lang_map.get(language, "plaintext"))

#################################################################
# Multi-Turn Dialogue & Document QA (using processed document context)
#################################################################
elif functionality == "Multi-Turn Dialogue & Document QA":
    st.subheader("Multi-Turn Dialogue")
    # Display conversation history
    history_text = get_history_text()
    if history_text:
        st.text_area("Conversation History", history_text, height=150, disabled=True)
    
    # Input for new message
    user_message = st.text_input("Your Message:", key="user_message")
    if st.button("Send"):
        add_to_history("user", user_message)
        dialogue_context = get_history_text()
        # If document context exists, append it to the prompt
        doc_context = st.session_state.document_context if st.session_state.document_context else "No document context available."
        full_prompt = f"{dialogue_context}\n\nDocument Context:\n{doc_context}\n\nRespond to the conversation above."
        final_prompt = apply_persona(full_prompt, persona_style)
        response = llm.generate_response(final_prompt)
        add_to_history("assistant", response)
        st.text_area("Updated Conversation", get_history_text(), height=150, disabled=True)
    
    st.markdown("### Document QA")
    user_question = st.text_input("Ask a question about the uploaded documents:")
    if st.button("Get Document Answer"):
        doc_answer = process_query_with_docs(user_question)
        st.write("Document Answer:", doc_answer)
