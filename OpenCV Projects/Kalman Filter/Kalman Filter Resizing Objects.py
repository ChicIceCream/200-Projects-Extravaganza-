import cv2
import mediapipe as mp
import numpy as np

class HandDetector:
    def __init__(self, detection_confidence=0.8):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_img)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return img

    def find_positions(self, img):
        left_hand = []
        right_hand = []
        height, width, _ = img.shape

        if self.results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(self.results.multi_hand_landmarks):
                hand_points = []
                for id, landmark in enumerate(hand_landmarks.landmark):
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    hand_points.append([cx, cy])

                if self.results.multi_handedness[idx].classification[0].label == "Left":
                    left_hand = hand_points
                else:
                    right_hand = hand_points

        return left_hand, right_hand

    def get_finger_states(self, hand_landmarks):
        if not hand_landmarks:
            return [False, False, False, False, False]

        fingers = []
        if hand_landmarks[4][0] > hand_landmarks[3][0]:
            fingers.append(True)
        else:
            fingers.append(False)

        for tip in [8, 12, 16, 20]:
            if hand_landmarks[tip][1] < hand_landmarks[tip - 2][1]:
                fingers.append(True)
            else:
                fingers.append(False)

        return fingers

class KalmanFilter:
    def __init__(self):
        self.kalman = cv2.KalmanFilter(4, 2)
        self.kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                                [0, 1, 0, 0]], np.float32)
        self.kalman.transitionMatrix = np.array([[1, 0, 1, 0],
                                                [0, 1, 0, 1],
                                                [0, 0, 1, 0],
                                                [0, 0, 0, 1]], np.float32)
        self.kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03
        self.last_position = None

    def predict(self):
        prediction = self.kalman.predict()
        return int(prediction[0]), int(prediction[1])

    def correct(self, position):
        if position:
            measurement = np.array(position, dtype=np.float32)
            self.kalman.correct(measurement)
            self.last_position = position
        return self.last_position

class DragRect:
    def __init__(self, pos_center, size=[200, 200]):
        self.pos_center = pos_center
        self.size = size
        self.color = (255, 0, 255)
        self.being_resized = False

    def update(self, left_cursor, right_cursor, left_fingers, right_fingers):
        cx, cy = self.pos_center
        w, h = self.size

        if (left_fingers[1] and sum(left_fingers) == 1 and 
            right_fingers[1] and sum(right_fingers) == 1):
            if self.is_point_inside(left_cursor) or self.is_point_inside(right_cursor):
                new_w = abs(right_cursor[0] - left_cursor[0])
                new_h = abs(right_cursor[1] - left_cursor[1])
                self.size = [max(100, new_w), max(100, new_h)]
                self.being_resized = True
                self.color = (0, 255, 0)
                return

        self.being_resized = False
        self.color = (255, 0, 255)

        if sum(left_fingers) >= 4 or sum(right_fingers) >= 4:
            cursor = left_cursor if sum(left_fingers) >= 4 else right_cursor
            if self.is_point_inside(cursor):
                self.pos_center = cursor

    def is_point_inside(self, point):
        if not point:
            return False
        cx, cy = self.pos_center
        w, h = self.size
        return (cx - w//2 < point[0] < cx + w//2 and 
                cy - h//2 < point[1] < cy + h//2)

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = HandDetector(detection_confidence=0.8)
    kalman_left = KalmanFilter()
    kalman_right = KalmanFilter()
    rect_list = [DragRect([x * 300 + 200, 200]) for x in range(3)]

    frame_interval = 3
    frame_count = 0

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        frame_count += 1

        if frame_count % frame_interval == 0:
            img = detector.find_hands(img)
            left_hand, right_hand = detector.find_positions(img)

            if left_hand:
                kalman_left.correct(left_hand[3])
            if right_hand:
                kalman_right.correct(right_hand[3])
        else:
            left_hand = [kalman_left.predict()]
            right_hand = [kalman_right.predict()]

        left_cursor = left_hand[0] if left_hand else None
        right_cursor = right_hand[0] if right_hand else None

        left_fingers = detector.get_finger_states(left_hand[0]) if left_hand else [False] * 5
        right_fingers = detector.get_finger_states(right_hand[0]) if right_hand else [False] * 5

        for rect in rect_list:
            rect.update(left_cursor, right_cursor, left_fingers, right_fingers)

        overlay = np.zeros_like(img, np.uint8)
        for rect in rect_list:
            cx, cy = rect.pos_center
            w, h = rect.size
            cv2.rectangle(overlay, 
                        (cx - w//2, cy - h//2),
                        (cx + w//2, cy + h//2),
                        rect.color, cv2.FILLED)

        alpha = 0.1
        mask = overlay.astype(bool)
        img[mask] = cv2.addWeighted(img, alpha, overlay, 1 - alpha, 0)[mask]

        cv2.imshow("Two-Handed Rectangle Control", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()