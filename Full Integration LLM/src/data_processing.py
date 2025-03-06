import logging
import pandas as pd
from io import BytesIO
from PyPDF2 import PdfReader
import streamlit as st

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
