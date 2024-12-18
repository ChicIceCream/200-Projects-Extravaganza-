import cv2
import mediapipe as mp
import numpy as np

class HandDetector:
    def __init__(self, detection_confidence=0.8):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,  # Set to False for video processing
            max_num_hands=2,         
            min_detection_confidence=detection_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def find_hands(self, img):
        # Convert BGR image to RGB (MediaPipe requires RGB)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process the image and detect hands
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
    
    def find_position(self, img):
        self.landmark_list = []
        height, width, _ = img.shape
        
        if self.results.multi_hand_landmarks:
            # Get the first detected hand
            hand = self.results.multi_hand_landmarks[0]
            
            # Process all landmarks in the hand
            for id, landmark in enumerate(hand.landmark):
                # Convert normalized coordinates to pixel coordinates
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                self.landmark_list.append([cx, cy])
                
        return self.landmark_list
    
    def find_distance(self, p1, p2, img):
        if len(self.landmark_list) > 0:
            x1, y1 = self.landmark_list[p1]
            x2, y2 = self.landmark_list[p2]
            
            # Calculate Euclidean distance
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            
            # Draw the points and line (optional)
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            
            return distance
        return None

class DragRect:
    def __init__(self, pos_center, size=[200, 200]):
        self.pos_center = pos_center
        self.size = size
        
    def update(self, cursor):
        cx, cy = self.pos_center
        w, h = self.size
        
        # Check if cursor (finger) is inside rectangle
        if cx - w//2 < cursor[0] < cx + w//2 and cy - h//2 < cursor[1] < cy + h//2:
            self.pos_center = cursor

def main():
    # Initialize camera
    cap = cv2.VideoCapture(0)  # Try 0, 1, or 2 depending on your camera
    cap.set(3, 1280)  # Width
    cap.set(4, 720)   # Height
    
    # Initialize hand detector
    detector = HandDetector(detection_confidence=0.8)
    
    # Create multiple rectangles
    rect_list = []
    for x in range(5):  # Create 5 rectangles
        rect_list.append(DragRect([x * 250 + 150, 150]))
    
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to grab frame")
            break
            
        # Flip image horizontally for more intuitive interaction
        img = cv2.flip(img, 1)
        
        # Find hand and its landmarks
        img = detector.find_hands(img)
        landmark_list = detector.find_position(img)
        
        if landmark_list:
            # Find distance between index (8) and thumv (4)
            distance = detector.find_distance(4, 8, img)
            
            if distance and distance < 50:  # If fingers are close together
                cursor = landmark_list[3]  # Use thumb tip as cursor
                # Update all rectangles
                for rect in rect_list:
                    rect.update(cursor)
        
        # Create transparent overlay
        overlay = np.zeros_like(img, np.uint8)
        for rect in rect_list:
            cx, cy = rect.pos_center
            w, h = rect.size
            # Draw rectangle on overlay
            cv2.rectangle(overlay, 
                        (cx - w//2, cy - h//2),
                        (cx + w//2, cy + h//2),
                        (0, 0, 255),
                        cv2.FILLED)
            # Draw corner rectangles
            thickness = 20
            corner_size = 40
            # Top left
            cv2.rectangle(overlay, 
                            (cx - w//2, cy - h//2),
                            (cx - w//2 + corner_size, cy - h//2 + thickness),
                            (0, 0, 255),
                            cv2.FILLED)
            cv2.rectangle(overlay,
                            (cx - w//2, cy - h//2),
                            (cx - w//2 + thickness, cy - h//2 + corner_size),
                            (0, 0, 255),
                            cv2.FILLED)
            # Similar rectangles for other corners...
        
        # Blend overlay with original image
        alpha = 0.2
        mask = overlay.astype(bool)
        img[mask] = cv2.addWeighted(img, alpha, overlay, 1 - alpha, 0)[mask]
        
        # Display result
        cv2.imshow("Draggable Rectangles", img)
        
        # Break loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()