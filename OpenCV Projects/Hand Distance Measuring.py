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
            max_num_hands=2,
            min_detection_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

    def calculate_distance(self, landmark1, landmark2, frame_width, frame_height):
        """Calculate Euclidean distance between two hand landmarks"""
        x1, y1 = int(landmark1.x * frame_width), int(landmark1.y * frame_height)
        x2, y2 = int(landmark2.x * frame_width), int(landmark2.y * frame_height)
        
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance, (x1, y1), (x2, y2)

    def process_frame(self, frame):
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame and detect hands
        results = self.hands.process(rgb_frame)
        
        # If hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
            
            # If two hands are detected, measure key distances
            if len(results.multi_hand_landmarks) == 2:
                hand1, hand2 = results.multi_hand_landmarks
                height, width, _ = frame.shape
                
                # Calculate distances between key points
                distances = {
                    'Thumb Tips': self.calculate_distance(hand1.landmark[4], hand2.landmark[4], width, height),
                    'Index Fingertips': self.calculate_distance(hand1.landmark[8], hand2.landmark[8], width, height),
                    'Palm Centers': self.calculate_distance(hand1.landmark[0], hand2.landmark[0], width, height)
                }
                
                # Draw distance lines and text
                for name, (dist, pt1, pt2) in distances.items():
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
                    midpoint = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
                    cv2.putText(frame, 
                                f"{name}: {dist:.2f} px", 
                                midpoint, 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                0.5, 
                                (255, 0, 0), 
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
        
        # Process frame and measure distances
        frame = measurer.process_frame(frame)
        
        # Display instructions
        cv2.putText(frame, 
                    "Show two hands to measure distances", 
                    (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, 
                    (0, 0, 255), 
                    2)
        
        # Show the frame
        cv2.imshow("Hand Distance Measurement", frame)
        
        # Break loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()