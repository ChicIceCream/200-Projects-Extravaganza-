import logging
import pandas as pd
import re
from io import BytesIO
from PyPDF2 import PdfReader
import streamlit as st

#* Existing document processing caching function
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

#* Additional Data Processing Functions

def remove_stopwords(text):
    # Basic implementation: remove common English stopwords
    stops = {"a", "an", "the", "is", "in", "on", "and", "or", "with", "of"}
    tokens = text.split()
    filtered_tokens = [word for word in tokens if word.lower() not in stops]
    return " ".join(filtered_tokens)

def normalize_text(text):
    # Lowercase and remove extra spaces
    return " ".join(text.lower().split())

def remove_special_characters(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

def tokenize_text(text):
    return text.split()
