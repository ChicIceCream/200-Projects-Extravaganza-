import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as palm
from huggingface_hub import InferenceClient

# **Load environment variables**
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("**GOOGLE_API_KEY** is missing in .env file.")
    st.stop()
if not HUGGINGFACE_API_KEY:
    st.error("**HUGGINGFACE_API_KEY** is missing in .env file.")
    st.stop()

# **Configure Gemini**
palm.configure(api_key=GOOGLE_API_KEY)

# **LLM Classes**

class GeminiLLM:
    def generate_response(self, prompt):
        response = palm.generate_text(
            model="models/text-bison-001",  # **Gemini model** identifier
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=200
        )
        return response.result if response.result else "No response."

class HuggingFaceLLM:
    def __init__(self, model_name, api_key):
        self.client = InferenceClient(provider="hf-inference", api_key=api_key)
        self.model_name = model_name

    def generate_response(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        completion = self.client.chat.completions.create(
            model=self.model_name, 
            messages=messages, 
            max_tokens=200,
        )
        return completion.choices[0].message

# **Sidebar** options for model selection and persona style
model_choice = st.sidebar.selectbox("Select **Model**", ["Gemini", "HuggingFace Llama"])
persona_style = st.sidebar.selectbox("Select **Persona Style**", ["Formal", "Professional", "Casual"])

# **Instantiate LLM** based on user choice
if model_choice == "Gemini":
    llm = GeminiLLM()
elif model_choice == "HuggingFace Llama":
    llm = HuggingFaceLLM("meta-llama/Llama-3.3-70B-Instruct", HUGGINGFACE_API_KEY)

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
    # **Simple preprocessing**: Lowercase as an example
    return text.lower()

st.title("**Arogo AI Assistant with Model & Persona Options**")

# **Sidebar** for selecting **NLP** functionalities
functionality = st.sidebar.selectbox("Choose **Functionality**", [
    "Home", "**Summarization**", "**Sentiment Analysis**", "**NER**", "**Question Answering**"
])

if functionality == "Home":
    st.write("Welcome to the **Arogo AI Streamlit App**. Use the sidebar to select a functionality.")

elif functionality == "**Summarization**":
    text_input = st.text_area("Enter text for **Summarization**:")
    if st.button("Summarize"):
        prompt = apply_persona(f"Summarize the following text concisely:\n{text_input}", persona_style)
        summary = llm.generate_response(prompt)
        st.write("**Summary:**", summary)

elif functionality == "**Sentiment Analysis**":
    text_input = st.text_area("Enter text for **Sentiment Analysis**:")
    if st.button("Analyze Sentiment"):
        prompt = apply_persona(f"Analyze the sentiment of the following text as positive, negative, or neutral:\n{text_input}", persona_style)
        sentiment = llm.generate_response(prompt)
        st.write("**Sentiment:**", sentiment)

elif functionality == "**NER**":
    text_input = st.text_area("Enter text for **Named Entity Recognition**:")
    if st.button("Extract Entities"):
        prompt = apply_persona(f"Extract and list the names, locations, and dates mentioned in the text:\n{text_input}", persona_style)
        entities = llm.generate_response(prompt)
        st.write("**Entities:**", entities)

elif functionality == "**Question Answering**":
    context = st.text_area("Enter **Context**:")
    question = st.text_input("Enter your **Question**:")
    if st.button("Get Answer"):
        prompt = apply_persona(f"Context: {context}\n\nQuestion: {question}\n\nAnswer:", persona_style)
        answer = llm.generate_response(prompt)
        st.write("**Answer:**", answer)
