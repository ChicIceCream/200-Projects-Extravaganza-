import streamlit as st
import os
import logging
from dotenv import load_dotenv
from llm_abstraction import Gemini, Groq, apply_persona, add_document_context
from data_processing import process_documents
from nlp_tasks import (
    init_chat_history,
    add_to_history,
    get_history_text,
    summarization_task,
    sentiment_analysis_task,
    ner_task,
    question_answering_task,
    code_generation_task,
    document_qa_task
)

#* Logging Setup

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Application startup.")

#* Load Environment Variables

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

#* Initialize LLM Based on Sidebar Selection

model_choice = st.sidebar.selectbox("Select Model", ["Gemini-1.5-Flash", "Llama-3.3-70b-Versatile"])
persona_style = st.sidebar.selectbox("Select Persona Style", ["Formal", "Professional", "Casual"])

if model_choice == "Gemini-1.5-Flash":
    llm = Gemini()
elif model_choice == "Llama-3.3-70b-Versatile":
    llm = Groq("llama-3.3-70b-versatile", GROQ_API_KEY)

#* Initialize Conversation and Document Context

init_chat_history()
if "document_context" not in st.session_state:
    st.session_state.document_context = ""

#* Sidebar: File Uploader for Documents (PDF, CSV, TXT)

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

#* Sidebar: Functionality Selection

functionality = st.sidebar.selectbox("Choose Functionality", [
    "Home", "Summarization", "Sentiment Analysis", "NER", "Question Answering", "Code Generation", "Multi-Turn Dialogue", "Document QA"
])

#* Streamlit UI for functionality selection

st.title("Full Integration LLM")

if functionality == "Home":
    st.write("Welcome to the last destination you will need for AI inference! Use the sidebar to select a functionality.")

elif functionality == "Summarization":
    text_input = st.text_area("Enter text for Summarization:")
    if st.button("Summarize"):
        output = summarization_task(text_input, persona_style, llm, st.session_state.document_context)
        logging.info("Summarization performed.")
        st.write("Summary:", output)
        
elif functionality == "Sentiment Analysis":
    text_input = st.text_area("Enter text for Sentiment Analysis:")
    if st.button("Analyze Sentiment"):
        output = sentiment_analysis_task(text_input, persona_style, llm, st.session_state.document_context)
        logging.info("Sentiment analysis performed.")
        st.write("Sentiment:", output)
        
elif functionality == "NER":
    text_input = st.text_area("Enter text for Named Entity Recognition:")
    if st.button("Extract Entities"):
        output = ner_task(text_input, persona_style, llm, st.session_state.document_context)
        logging.info("NER performed.")
        st.write("Entities:", output)
        
elif functionality == "Question Answering":
    context = st.text_area("Enter Context:")
    question = st.text_input("Enter your Question:")
    if st.button("Get Answer"):
        output = question_answering_task(context, question, persona_style, llm, st.session_state.document_context)
        logging.info("Question Answering performed.")
        st.write("Answer:", output)
        
elif functionality == "Code Generation":
    code_description = st.text_area("Enter description for code generation:")
    language = st.selectbox("Select Language", ["Python", "JavaScript", "Java", "C++", "Other"])
    lang_map = {
        "Python": "python",
        "JavaScript": "javascript",
        "Java": "java",
        "C++": "cpp",
        "Other": "Other"
    }
    if st.button("Generate Code"):
        output = code_generation_task(code_description, language, persona_style, llm, st.session_state.document_context)
        logging.info("Code Generation performed.")
        st.code(output, language=lang_map.get(language, "plaintext"))

#* Streamlit UI for multi turn dialogue

elif functionality == "Multi-Turn Dialogue":
    st.subheader("Multi-Turn Dialogue")
    history_text = get_history_text()
    if history_text:
        st.text_area("Conversation History", history_text, height=150, disabled=True)
    
    user_message = st.text_input("Your Message:", key="user_message")
    if st.button("Send"):
        add_to_history("user", user_message)
        dialogue_context = get_history_text()
        
        final_prompt = apply_persona(dialogue_context + "\n\nRespond to the conversation above.", persona_style)
        response = llm.generate_response(final_prompt)
        add_to_history("assistant", response)
        logging.info("Multi-turn dialogue message sent.")
        st.text_area("Updated Conversation", get_history_text(), height=150, disabled=True)

#* Streamlit UI for Document Q & A

elif functionality == "Document QA":
    st.subheader("Document QA")
    user_question = st.text_input("Ask a question about the uploaded documents:")
    if st.button("Get Document Answer"):
        output = document_qa_task(st.session_state.document_context, user_question)
        logging.info("Document QA performed.")
        st.write("Document Answer:", output)

logging.info("Application operations completed for this session.")
