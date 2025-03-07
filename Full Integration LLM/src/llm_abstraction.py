import logging
import requests
from google import generativeai as genai

class Gemini:
    def generate_response(self, prompt):
        logging.info("Generating response using Gemini.")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([prompt])
        return response.text

class Groq:
    def __init__(self, model_name, api_key):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"
    
    def generate_response(self, prompt):
        logging.info("Generating response using Groq.")
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

def apply_persona(prompt, persona):
    if persona == "Formal":
        return f"Please respond in a formal tone. {prompt}"
    elif persona == "Professional":
        return f"Please answer in a professional manner. {prompt}"
    elif persona == "Casual":
        return f"Answer casually: {prompt}"
    return prompt

def add_document_context(prompt, document_context):
    if document_context.strip():
        return f"{prompt}\n\nDocument Context:\n{document_context}"
    return prompt
