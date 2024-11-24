import cv2
import mediapipe as mp
import numpy as np

class HandDetector:
    def __init__(self, detection_confidence=0.8):
        # Initialize MediaPipe Hands with support for multiple hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,          # Changed to 2 to detect both hands
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def find_hands(self, img):
        # Convert BGR image to RGB
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_img)
        
        # Draw hand landmarks if detected
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
        return img
    
    def find_positions(self, img):
        """Returns landmarks for both hands separately"""
        left_hand = []
        right_hand = []
        height, width, _ = img.shape
        
        if self.results.multi_hand_landmarks:
            # Process each detected hand
            for idx, hand_landmarks in enumerate(self.results.multi_hand_landmarks):
                hand_points = []
                for id, landmark in enumerate(hand_landmarks.landmark):
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    hand_points.append([cx, cy])
                
                # Determine if it's left or right hand
                if self.results.multi_handedness[idx].classification[0].label == "Left":
                    left_hand = hand_points
                else:
                    right_hand = hand_points
                    
        return left_hand, right_hand
    
    def get_finger_states(self, hand_landmarks):
        """
        Determines which fingers are up in a hand
        Returns list of booleans [thumb, index, middle, ring, pinky]
        """
        if not hand_landmarks:
            return [False, False, False, False, False]
        
        fingers = []
        
        # Thumb (comparing horizontal position)
        if hand_landmarks[4][0] > hand_landmarks[3][0]:
            fingers.append(True)
        else:
            fingers.append(False)
            
        # Other fingers (comparing vertical position)
        for tip in [8, 12, 16, 20]:  # Index, Middle, Ring, Pinky tips
            if hand_landmarks[tip][1] < hand_landmarks[tip-2][1]:
                fingers.append(True)
            else:
                fingers.append(False)
                
        return fingers

class DragRect:
    def __init__(self, pos_center, size=[200, 200]):
        self.pos_center = pos_center
        self.size = size
        self.color = (255, 0, 255)  # Default color
        self.being_resized = False
        
    def update(self, left_cursor, right_cursor, left_fingers, right_fingers):
        cx, cy = self.pos_center
        w, h = self.size
        
        # Check for resize gesture (both hands with index fingers up)
        if (left_fingers[1] and sum(left_fingers) == 1 and 
            right_fingers[1] and sum(right_fingers) == 1):
            if self.is_point_inside(left_cursor) or self.is_point_inside(right_cursor):
                # Calculate new size based on distance between hands
                new_w = abs(right_cursor[0] - left_cursor[0])
                new_h = abs(right_cursor[1] - left_cursor[1])
                self.size = [max(100, new_w), max(100, new_h)]
                self.being_resized = True
                self.color = (0, 255, 0)  # Green while resizing
                return
                
        self.being_resized = False
        self.color = (255, 0, 255)  # Reset color
        
        # Check for drag gesture (all fingers up on either hand)
        if sum(left_fingers) >= 4 or sum(right_fingers) >= 4:
            cursor = left_cursor if sum(left_fingers) >= 4 else right_cursor
            if self.is_point_inside(cursor):
                self.pos_center = cursor
                
    def is_point_inside(self, point):
        if not point:  # If point is None or empty
            return False
        cx, cy = self.pos_center
        w, h = self.size
        return (cx - w//2 < point[0] < cx + w//2 and 
                cy - h//2 < point[1] < cy + h//2)

def main():
    # Initialize camera
    cap = cv2.VideoCapture(0)  # Try 0, 1, or 2 depending on your camera
    cap.set(3, 1280)  # Width
    cap.set(4, 720)   # Height
    
    # Initialize hand detector
    detector = HandDetector(detection_confidence=0.8)
    
    # Create rectangles
    rect_list = []
    for x in range(3):  # Reduced to 3 rectangles for better visibility
        rect_list.append(DragRect([x * 300 + 200, 200]))
    
    # Add text overlay function
    def put_instruction_text(img, text, pos, scale=1):
        cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, 
                    (255, 255, 255), 2, cv2.LINE_AA)
    
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to grab frame")
            break
            
        # Flip image horizontally
        img = cv2.flip(img, 1)
        
        # Find hands and landmarks
        img = detector.find_hands(img)
        left_hand, right_hand = detector.find_positions(img)
        
        # Get finger states for both hands
        left_fingers = detector.get_finger_states(left_hand)
        right_fingers = detector.get_finger_states(right_hand)
        
        # Get cursors (index fingertips) for both hands
        left_cursor = left_hand[3] if left_hand else None
        right_cursor = right_hand[3] if right_hand else None
        
        # Update rectangles
        for rect in rect_list:
            rect.update(left_cursor, right_cursor, left_fingers, right_fingers)
        
        # Create transparent overlay
        overlay = np.zeros_like(img, np.uint8)
        for rect in rect_list:
            cx, cy = rect.pos_center
            w, h = rect.size
            # Draw main rectangle
            cv2.rectangle(overlay, 
                        (cx - w//2, cy - h//2),
                        (cx + w//2, cy + h//2),
                        rect.color,
                        cv2.FILLED)
            
            # Draw corner indicators
            thickness = 20
            corner_size = 40
            for x in [-1, 1]:
                for y in [-1, 1]:
                    cv2.rectangle(overlay,
                                (cx + x*w//2 - x*corner_size*(x+1)//2,
                                    cy + y*h//2 - y*corner_size*(y+1)//2),
                                (cx + x*w//2 + x*thickness*(-x+1)//2,
                                    cy + y*h//2 + y*thickness*(-y+1)//2),
                                rect.color,
                                cv2.FILLED)
        
        # Blend overlay with original image
        alpha = 0.1
        mask = overlay.astype(bool)
        img[mask] = cv2.addWeighted(img, alpha, overlay, 1 - alpha, 0)[mask]
        
        # Add instruction text
        put_instruction_text(img, "Raise all fingers to drag", (20, 30))
        put_instruction_text(img, "Use both index fingers to resize", (20, 70))
        
        # Display result
        cv2.imshow("Two-Handed Rectangle Control", img)
        
        # Break loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()