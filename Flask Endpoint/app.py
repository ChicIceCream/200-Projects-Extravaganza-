from flask import Flask, Response, jsonify
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
import threading
import time


app = Flask(__name__)

# Initialize once when the app starts
capture = cv2.VideoCapture(0)  # Camera input
model = keras.model.load_model('keras_model.h5', compile=False)
class_names = [line.strip() for line in open("labels.txt", "r")]

# Shared variables
latest_class = ""
latest_confidence = 0

def process_frame(frame):
    global latest_class, latest_confidence
    
    # Preprocessing
    resized_frame = cv2.resize(frame, (224, 224))
    image_array = (resized_frame.astype(np.float32) / 127.5) - 1
    prediction = model.predict(np.expand_dims(image_array, axis=0))
    
    # Update results
    index = np.argmax(prediction)
    latest_class = class_names[index]
    latest_confidence = int(np.round(prediction[0][index] * 100))

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            ret, frame = capture.read()
            if not ret:
                break
                
            # Process the frame (this will block other requests!)
            process_frame(frame)
            
            # Add overlay to frame
            display_frame = cv2.resize(frame, (640, 480))
            text = f"{latest_class} ({latest_confidence}%)"
            cv2.putText(display_frame, text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # Encode as JPEG
            _, buffer = cv2.imencode('.jpg', display_frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/prediction')
def prediction():
    return jsonify({
        'class': latest_class,
        'confidence': latest_confidence
    })

# Keep the same HTML template
@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Keras Model Prediction</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin: 20px; }
            .container { max-width: 800px; margin: 0 auto; }
            .video-container { margin: 20px 0; }
            .prediction { font-size: 24px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Keras Model Prediction</h1>
            <div class="video-container">
                <img src="/video_feed" width="640" height="480">
            </div>
            <div class="prediction" id="prediction">
                Class: Loading..., Confidence: 0%
            </div>
        </div>
        <script>
            // Update prediction text every second
            setInterval(function() {
                fetch('/prediction')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('prediction').innerText = 
                            `Class: ${data.class}, Confidence: ${data.confidence}%`;
                    });
            }, 1000);
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=False)
