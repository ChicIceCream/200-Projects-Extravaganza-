import cv2
import numpy as np
from tensorflow import keras

# Use DirectShow backend for Windows if needed
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Load the Keras model and labels
model = keras.models.load_model('C:\\Users\\User\\Desktop\\python_in_vs\\200 Projects!\\Flask Endpoint\\keras_model.h5')
class_names = [line.strip() for line in open("C:\\Users\\User\\Desktop\\python_in_vs\\200 Projects!\\Flask Endpoint\\labels.txt", "r").readlines()]

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Resize and preprocess the frame for prediction
    resized_frame = cv2.resize(frame, (224, 224))
    image_array = np.asarray(resized_frame, dtype=np.float32).reshape(1, 224, 224, 3)
    image_array = (image_array / 127.5) - 1

    # Make prediction
    prediction = model.predict(image_array)
    index = np.argmax(prediction)
    confidence = int(np.round(prediction[0][index] * 100))
    label = class_names[index]

    # Overlay prediction text on the original frame
    text = f"Class: {label}, Confidence: {confidence}%"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Video Feed", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
