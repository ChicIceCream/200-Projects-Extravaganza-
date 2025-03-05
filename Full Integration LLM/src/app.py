import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from transformers import pipeline

# **Load environment variables** from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("**GOOGLE_API_KEY** is missing in .env file.")
    st.stop()

# **Configure Gemini**
genai.configure(api_key=GOOGLE_API_KEY)

class GeminiLLM:
    def generate_response(self, prompt):
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # calling my model
        response = model.generate_content([prompt])
        
        return response.text

class HuggingFaceLLM:
    def __init__(self, model_name):
        self.generator = pipeline("text-generation", model=model_name)
    def generate_response(self, prompt):
        response = self.generator(prompt, max_length=200, do_sample=True)
        return response[0]["generated_text"]

# **Instantiate Gemini LLM**
llm = GeminiLLM()

model_choice = st.sidebar.selectbox("Select **Model**", ["Gemini", "HuggingFace GPT-2", "HuggingFace GPT-Neo"])
persona_style = st.sidebar.selectbox("Select **Persona Style**", ["Formal", "Professional", "Casual"])

# **Instantiate LLM** based on user choice
if model_choice == "Gemini":
    llm = GeminiLLM()
elif model_choice == "HuggingFace GPT-2":
    llm = HuggingFaceLLM("gpt2")
elif model_choice == "HuggingFace GPT-Neo":
    llm = HuggingFaceLLM("EleutherAI/gpt-neo-125M")

def apply_persona(prompt, persona):
    # **Prepend style instructions** based on selected persona
    if persona == "Formal":
        return f"Please respond in a formal tone. {prompt}"
    elif persona == "Professional":
        return f"Please answer in a professional manner. {prompt}"
    elif persona == "Casual":
        return f"Answer casually: {prompt}"
    return prompt


def preprocess_text(text):
    # **Preprocessing**: Lowercase as an example
    return text.lower()

st.title("**Arogo AI Assistant with Gemini**")

# **Sidebar** for selecting **NLP** tasks
functionality = st.sidebar.selectbox("Choose Functionality", [
    "Home", "Summarization", "Sentiment Analysis", "NER", "Question Answering"
])

if functionality == "Home":
    st.write("Welcome to the **Arogo AI Streamlit App**. Use the sidebar to select a functionality.")
    
elif functionality == "Summarization":
    text_input = st.text_area("Enter text for **Summarization**:")
    if st.button("Summarize"):
        prompt = f"Summarize the following text concisely:\n{text_input}"
        summary = llm.generate_response(prompt)
        st.write("**Summary:**", summary)
        
elif functionality == "**Sentiment Analysis**":
    text_input = st.text_area("Enter text for **Sentiment Analysis**:")
    if st.button("Analyze Sentiment"):
        prompt = f"Analyze the sentiment of the following text as positive, negative, or neutral:\n{text_input}"
        sentiment = llm.generate_response(prompt)
        st.write("**Sentiment:**", sentiment)
        
elif functionality == "**NER**":
    text_input = st.text_area("Enter text for **Named Entity Recognition**:")
    if st.button("Extract Entities"):
        prompt = f"Extract and list the names, locations, and dates mentioned in the text:\n{text_input}"
        entities = llm.generate_response(prompt)
        st.write("**Entities:**", entities)
        
elif functionality == "**Question Answering**":
    context = st.text_area("Enter **Context**:")
    question = st.text_input("Enter your **Question**:")
    if st.button("Get Answer"):
        prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        answer = llm.generate_response(prompt)
        st.write("**Answer:**", answer)