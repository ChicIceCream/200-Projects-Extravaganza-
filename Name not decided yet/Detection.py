import cv2
import mediapipe as mp
import subprocess
import os

# Initialize Mediapipe for hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Function to detect thumbs up gesture
def is_thumbs_up(landmarks):
    # Define thumb tip and index tip points
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    # Check if thumb is above the other fingers (basic logic for thumbs up detection)
    if (
        thumb_tip.y < landmarks[mp_hands.HandLandmark.THUMB_IP].y and
        thumb_tip.y < landmarks[mp_hands.HandLandmark.THUMB_MCP].y and
        thumb_tip.x < index_tip.x  # Assuming thumbs-up is made with the right hand
    ):
        return True
    return False

# Function to send an image to LLaVA for inference
def infer_with_llava(image_path):
    # Run Ollama LLaVA with the image input
    result = subprocess.run(
        ["ollama", "run", "llava", "--image", image_path],
        capture_output=True,
        text=True
    )
    return result.stdout

# Main camera processing loop
def main():
    cap = cv2.VideoCapture(0)  # Open the default camera (ID=0)
    print("Press 'q' to quit.")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a mirror view
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB for Mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw hand landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Check for thumbs up gesture
                if is_thumbs_up(hand_landmarks.landmark):
                    print("Thumbs up detected! Capturing frame for inference...")
                    
                    # Save the frame to a temporary file
                    image_path = "temp_frame.jpg"
                    cv2.imwrite(image_path, frame)

                    # Run inference with LLaVA
                    output = infer_with_llava(image_path)
                    print("Inference Output:")
                    print(output)

        # Display the video feed
        cv2.imshow("Camera Feed", frame)

        # Break the loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    hands.close()

if __name__ == "__main__":
    main()
