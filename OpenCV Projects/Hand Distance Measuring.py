import cv2
import mediapipe as mp
import numpy as np
import math

class HandDistanceMeasurer:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

    def calculate_hand_depth(self, hand_landmarks, frame_width, frame_height):
        """
        Estimate hand depth from camera
        Uses the relative size of landmarks and their vertical position
        """
        # Get vertical range of hand
        y_coordinates = [landmark.y for landmark in hand_landmarks.landmark]
        hand_height = max(y_coordinates) - min(y_coordinates)
        
        # Get horizontal spread of hand
        x_coordinates = [landmark.x for landmark in hand_landmarks.landmark]
        hand_width = max(x_coordinates) - min(x_coordinates)
        
        # Estimate distance based on hand size in frame
        # These factors are approximate and may need calibration
        distance_cm = 50 / (hand_height * frame_height)  # Vertical depth estimation
        width_distance = 50 / (hand_width * frame_width)  # Horizontal depth estimation
        
        return (distance_cm + width_distance) / 2  # Average of both estimates

    def process_frame(self, frame):
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame and detect hands
        results = self.hands.process(rgb_frame)
        
        # If a hand is detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Calculate and display depth
                height, width, _ = frame.shape
                depth = self.calculate_hand_depth(hand_landmarks, width, height)
                
                # Display depth information
                cv2.putText(frame, 
                            f"Estimated Distance: {depth:.2f} cm", 
                            (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            1, 
                            (0, 255, 0), 
                            2)
        
        return frame

def main():
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    # Create hand distance measurer
    measurer = HandDistanceMeasurer()
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # Flip frame horizontally
        frame = cv2.flip(frame, 1)
        
        # Process frame and measure distance
        frame = measurer.process_frame(frame)
        
        # Display additional instructions
        cv2.putText(frame, 
                    "Move hand closer/further from camera", 
                    (10, frame.shape[0] - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, 
                    (255, 0, 0), 
                    1)
        
        # Show the frame
        cv2.imshow("Hand to Screen Distance", frame)
        
        # Break loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

    ######################### Code by Abhivyakt Bhati ############################