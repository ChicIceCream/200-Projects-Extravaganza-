import streamlit as st
import requests
import time
import cv2
from PIL import Image
import io

# Configure the app
st.set_page_config(page_title="Keras Model Prediction", layout="wide")
st.title("Keras Model Prediction")

# URL of the Flask API
FLASK_URL = "http://localhost:5000"

# Function to get the latest prediction
def get_prediction():
    try:
        response = requests.get(f"{FLASK_URL}/prediction")
        return response.json()
    except:
        return {"class": "Error connecting to server", "confidence": 0}

# Create placeholders for dynamic content
video_placeholder = st.empty()
prediction_placeholder = st.empty()

# Main app loop
while True:
    # Get the latest prediction
    prediction = get_prediction()
    
    # Update the prediction display
    prediction_placeholder.markdown(f"""
    ## Prediction Results
    - **Class**: {prediction['class']}
    - **Confidence**: {prediction['confidence']}%
    """)
    
    # Try to get the latest video frame
    try:
        response = requests.get(f"{FLASK_URL}/video_feed", stream=True, timeout=0.5)
        if response.status_code == 200:
            # Extract the JPEG frame from the multipart response
            for chunk in response.iter_content(chunk_size=1024):
                if chunk.startswith(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'):
                    jpeg_data = chunk.split(b'\r\n\r\n')[1].split(b'\r\n')[0]
                    image = Image.open(io.BytesIO(jpeg_data))
                    video_placeholder.image(image, caption="Live Video Feed", use_column_width=True)
                    break
    except:
        video_placeholder.error("Could not connect to video feed")
    
    # Small delay to avoid too many requests
    time.sleep(0.5)