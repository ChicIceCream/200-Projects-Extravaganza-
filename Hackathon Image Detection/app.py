from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import time

# Load environment variables
load_dotenv()

# Configure the generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Using Gemini API to get a response
def get_gemini_response(input_text, image):
    '''
    This function will load the Gemini model and get responses
    '''
    if input_text:
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(image)
    
    if response and response.parts:
        return response.parts[0].text
    else:
        return "No valid response returned by the model."

# Function to display text in a streaming manner by chunks
def stream_response(response_text, chunk_size=14):
    placeholder = st.empty()
    words = response_text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    
    text = ""
    for chunk in chunks:
        for letter in chunk:
            text += letter
            placeholder.text(text)
            time.sleep(0.01)  # Adjust the speed of letter streaming here
        text += "\n\n"
        placeholder.text(text)
        time.sleep(0.5)  # Adjust the speed of chunk streaming here

# Set up Streamlit application
st.set_page_config(page_title="Image Application Demo")

st.header("Image Detection")

input_text ='''
Give me all the details I would need to know for finding this device. Include the brand,\n
model, and any other relevant information. Give it in single keywords. Give me all the \n
details I would need to know for finding this device. 
'''

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

submit = st.button("Tell me about the image")

# When submit is clicked
if submit:
    with st.spinner('Generating response...'):
        response = get_gemini_response(input_text, image)
    st.header("The response to your question is: ")
    stream_response(response)
