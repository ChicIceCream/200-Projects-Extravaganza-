import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import pyttsx3
import threading
from queue import Queue
import time

class GestureObjectRecognition:
    def __init__(self):
        # Initialize video capture
        self.cap = cv2.VideoCapture(0)
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Initialize MobileNetV2 for object recognition
        print("Loading MobileNetV2 model...")
        self.model = MobileNetV2(weights='imagenet')
        print("Model loaded successfully!")
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Queue for speech outputs
        self.speech_queue = Queue()
        
        # Status indicators
        self.inference_active = False
        self.last_inference_time = time.time()
        
        # Start speech thread
        self.speech_thread = threading.Thread(target=self.speech_worker, daemon=True)
        self.speech_thread.start()
        
        print("System initialized and ready!")
        print("Show thumbs up gesture to trigger object recognition.")
        print("Press 'q' to quit.")
    
    def speech_worker(self):
        while True:
            text = self.speech_queue.get()
            self.engine.say(text)
            self.engine.runAndWait()
            self.speech_queue.task_done()
    
    def detect_thumbs_up(self, hand_landmarks):
        if hand_landmarks:
            # Get all relevant landmark points
            thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
            thumb_ip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP]
            thumb_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_MCP]
            
            # Get index finger landmarks for reference
            index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
            
            # Check other fingers
            other_fingers_tips = [
                hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP],
                hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP],
                hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
            ]
            
            other_fingers_mcp = [
                hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP],
                hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
                hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP],
                hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP]
            ]
            
            # Conditions for thumbs up:
            # 1. Thumb should be extending upwards
            thumb_is_up = (thumb_tip.y < thumb_ip.y < thumb_mcp.y)
            
            # 2. Other fingers should be folded (tips should be below their MCP joints)
            fingers_folded = all(
                tip.y > mcp.y 
                for tip, mcp in zip(other_fingers_tips, other_fingers_mcp)
            )
            
            # 3. Additional check for thumb orientation
            thumb_is_vertical = abs(thumb_tip.x - thumb_mcp.x) < 0.1  # Threshold for vertical alignment
            
            # Debug output
            if thumb_is_up and fingers_folded:
                print("Potential thumbs up detected!")
                print(f"Thumb vertical: {thumb_is_vertical}")
                print(f"Fingers folded: {fingers_folded}")
            
            return thumb_is_up and fingers_folded and thumb_is_vertical

        return False
    
    def predict_object(self, frame):
        print("Starting inference...")
        self.inference_active = True
        
        # Resize and preprocess the image
        img = cv2.resize(frame, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        
        # Make prediction
        predictions = self.model.predict(img, verbose=0)
        results = decode_predictions(predictions, top=1)[0]
        
        self.inference_active = False
        print(f"Inference complete! Detected: {results[0][1]} ({results[0][2]:.1%} confidence)")
        
        return results[0][1], results[0][2]
    
    def draw_status_overlay(self, frame):
        # Add status overlay to frame
        overlay = frame.copy()
        
        # Status box
        cv2.rectangle(overlay, (10, 10), (300, 90), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # Status text
        cv2.putText(frame, "Status:", (20, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        if self.inference_active:
            status = "PROCESSING..."
            color = (0, 255, 255)  # Yellow
        else:
            status = "Ready - Show thumbs up!"
            color = (0, 255, 0)    # Green
            
        cv2.putText(frame, status, (20, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        # Add cooldown indicator
        cooldown_remaining = max(0, 2 - (time.time() - self.last_inference_time))
        if cooldown_remaining > 0:
            cv2.putText(frame, f"Cooldown: {cooldown_remaining:.1f}s", (20, 85),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
    
    def run(self):
        cooldown = 2  # Cooldown in seconds between predictions
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Cannot read from camera!")
                break
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            # Draw hand landmarks and check for gesture
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    current_time = time.time()
                    if (self.detect_thumbs_up(hand_landmarks) and 
                        current_time - self.last_inference_time > cooldown):
                        
                        # Save frame and timestamp
                        cv2.imwrite('captured_frame.jpg', frame)
                        print("Frame captured! Starting object recognition...")
                        
                        # Predict object
                        label, confidence = self.predict_object(frame)
                        
                        # Format and queue speech output
                        text = f"I see a {label} with {confidence:.1%} confidence"
                        self.speech_queue.put(text)
                        
                        self.last_inference_time = current_time
            
            # Draw status overlay
            self.draw_status_overlay(frame)
            
            # Display frame
            cv2.imshow('Object Recognition', frame)
            
            # Break loop on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nShutting down...")
                break
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    recognizer = GestureObjectRecognition()
    recognizer.run()