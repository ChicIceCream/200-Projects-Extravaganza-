import cv2
import mediapipe as mp
import itertools
import numpy as np
from scipy.interpolate import splev, splprep

class MakeupApplication:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        # Initialize mediapipe solutions
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=min_detection_confidence,
                                                    min_tracking_confidence=min_tracking_confidence)

        # Precompute index lists for facial landmarks
        self.LEFT_EYE_INDEXES = list(set(itertools.chain(*self.mp_face_mesh.FACEMESH_LEFT_EYE)))
        self.RIGHT_EYE_INDEXES = list(set(itertools.chain(*self.mp_face_mesh.FACEMESH_RIGHT_EYE)))
        self.LIPS_INDEXES = list(set(itertools.chain(*self.mp_face_mesh.FACEMESH_LIPS)))
        self.LEFT_EYEBROW_INDEXES = list(set(itertools.chain(*self.mp_face_mesh.FACEMESH_LEFT_EYEBROW)))
        self.RIGHT_EYEBROW_INDEXES = list(set(itertools.chain(*self.mp_face_mesh.FACEMESH_RIGHT_EYEBROW)))

    def get_upper_side_coordinates(self, eye_landmarks):
        sorted_landmarks = sorted(eye_landmarks, key=lambda coord: coord.y)
        half_length = len(sorted_landmarks) // 2
        return sorted_landmarks[:half_length]

    def get_lower_side_coordinates(self, eye_landmarks):
        sorted_landmarks = sorted(eye_landmarks, key=lambda coord: coord.y)
        half_length = len(sorted_landmarks) // 2
        return sorted_landmarks[half_length:]

    def apply_eyeshadow(self, image, eye_landmarks, eyebrow_landmarks, color, blur_kernel_size=(7, 7), blur_sigma=10, color_intensity=0.4):
        eye_points = np.array([(int(landmarks.x * image.shape[1]), int(landmarks.y * image.shape[0])) for landmarks in eye_landmarks])
        eyebrow_points = np.array([(int(landmarks.x * image.shape[1]), int(landmarks.y * image.shape[0])) for landmarks in eyebrow_landmarks])
        upper_eye_points = np.array([(int(landmarks.x * image.shape[1]), int(landmarks.y * image.shape[0])) for landmarks in self.get_upper_side_coordinates(eye_landmarks)])

        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        combined_points = np.concatenate([upper_eye_points, eyebrow_points[::-1]])
        cv2.fillPoly(mask, [cv2.convexHull(combined_points)], 255)

        colored_image = np.zeros_like(image)
        colored_image[:] = color

        eyeshadow_image = cv2.bitwise_and(colored_image, colored_image, mask=mask)
        eye_shadow_colored = cv2.addWeighted(image, 1, eyeshadow_image, color_intensity, 0)

        blurred = cv2.GaussianBlur(eye_shadow_colored, blur_kernel_size, blur_sigma)

        gradient_mask = cv2.GaussianBlur(mask, (15, 15), 0)
        gradient_mask = gradient_mask / 255.0
        eyeshadow_with_gradient = (blurred * gradient_mask[..., np.newaxis] + image * (1 - gradient_mask[..., np.newaxis])).astype(np.uint8)

        final_image = np.where(mask[..., np.newaxis] == 0, image, eyeshadow_with_gradient)
        return final_image

    def apply_lipstick(self, image, landmarks, indexes, color, blur_kernel_size=(7, 7), blur_sigma=10, color_intensity=0.4):
        points = np.array([(int(landmarks[idx].x * image.shape[1]), int(landmarks[idx].y * image.shape[0])) for idx in indexes])

        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [cv2.convexHull(points)], 255)

        boundary_mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)

        colored_image = np.zeros_like(image)
        colored_image[:] = color

        lipstick_image = cv2.bitwise_and(colored_image, colored_image, mask=boundary_mask)
        lips_colored = cv2.addWeighted(image, 1, lipstick_image, color_intensity, 0)

        blurred = cv2.GaussianBlur(lips_colored, blur_kernel_size, blur_sigma)

        gradient_mask = cv2.GaussianBlur(boundary_mask, (15, 15), 0)
        gradient_mask = gradient_mask / 255.0
        lips_with_gradient = (blurred * gradient_mask[..., np.newaxis] + image * (1 - gradient_mask[..., np.newaxis])).astype(np.uint8)

        final_image = np.where(boundary_mask[..., np.newaxis] == 0, image, lips_with_gradient)
        return final_image

    def draw_eyeliner(self, image, upper_eye_coordinates, color=(14, 14, 18), thickness=1):
        result_image = image.copy()

        eyeliner_points = [(int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])) for landmark in upper_eye_coordinates]

        eyeliner_points.sort(key=lambda x: x[0])

        eyeliner_points = np.array(eyeliner_points, dtype=np.int32)

        for i in range(len(eyeliner_points) - 1):
            start_point = tuple(eyeliner_points[i])
            end_point = tuple(eyeliner_points[i + 1])
            cv2.line(result_image, start_point, end_point, color, thickness)

        return result_image

    def apply_blush(self, image, face_landmarks, cheek_indices, chin_index, color=(128, 0, 128), intensity=0.6, size_multiplier=1.0):
        result_image = image.copy()
        img_height, img_width = image.shape[:2]

        def get_coords(index):
            landmark = face_landmarks.landmark[index]
            return np.array([int(landmark.x * img_width), int(landmark.y * img_height)])

        def compute_blush_parameters(cheek_idx, chin_idx):
            cheek_coords = get_coords(cheek_idx)
            chin_coords = get_coords(chin_idx)

            center_coords = cheek_coords + 0.3 * (chin_coords - cheek_coords)
            center_coords = center_coords.astype(int)

            distance = np.linalg.norm(cheek_coords - chin_coords)
            axes_length = (int(distance * 0.6 * size_multiplier), int(distance * 0.3 * size_multiplier))

            y_min = max(center_coords[1] - axes_length[1], cheek_coords[1] - 20)
            y_max = min(center_coords[1] + axes_length[1], chin_coords[1] - 20)
            axes_length = (axes_length[0], (y_max - y_min) // 2)
            center_coords[1] = (y_min + y_max) // 2

            return center_coords, axes_length

        left_center, left_axes = compute_blush_parameters(cheek_indices[0], chin_index)
        right_center, right_axes = compute_blush_parameters(cheek_indices[1], chin_index)

        blush_mask = np.zeros((img_height, img_width), dtype=np.uint8)
        cv2.ellipse(blush_mask, tuple(left_center), left_axes, 0, 0, 360, 255, -1)
        cv2.ellipse(blush_mask, tuple(right_center), right_axes, 0, 0, 360, 255, -1)

        blurred_mask = cv2.GaussianBlur(blush_mask, (99, 99), 0)
        normalized_mask = blurred_mask / 255.0
        normalized_mask = normalized_mask[..., np.newaxis]

        blush_color_image = np.full_like(image, color)

        blended_image = (image * (1 - normalized_mask * intensity) + blush_color_image * (normalized_mask * intensity)).astype(np.uint8)

        return blended_image

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = self.face_mesh.process(rgb_frame)
        rgb_frame.flags.writeable = True

        if results.multi_face_landmarks:
            for face_no, face_landmarks in enumerate(results.multi_face_landmarks):
                left_eye_landmarks = [face_landmarks.landmark[idx] for idx in self.LEFT_EYE_INDEXES]
                left_eyebrow_landmarks = [face_landmarks.landmark[idx] for idx in self.LEFT_EYEBROW_INDEXES]
                upper_left_eye_coordinates = self.get_upper_side_coordinates(left_eye_landmarks)
                lower_left_eyebrow = self.get_lower_side_coordinates(left_eyebrow_landmarks)
                frame = self.apply_eyeshadow(frame, upper_left_eye_coordinates, lower_left_eyebrow, (170, 80, 160))

                right_eye_landmarks = [face_landmarks.landmark[idx] for idx in self.RIGHT_EYE_INDEXES]
                right_eyebrow_landmarks = [face_landmarks.landmark[idx] for idx in self.RIGHT_EYEBROW_INDEXES]
                upper_right_eye_coordinates = self.get_upper_side_coordinates(right_eye_landmarks)
                lower_right_eyebrow = self.get_lower_side_coordinates(right_eyebrow_landmarks)
                frame = self.apply_eyeshadow(frame, upper_right_eye_coordinates, lower_right_eyebrow, (170, 80, 160))

                frame = self.draw_eyeliner(frame, upper_left_eye_coordinates)
                frame = self.draw_eyeliner(frame, upper_right_eye_coordinates)

                frame = self.apply_lipstick(frame, face_landmarks.landmark, self.LIPS_INDEXES, (0, 0, 255))

                cheek_indices = [234, 454]
                chin_index = 152
                # frame = self.apply_blush(frame, face_landmarks, cheek_indices, chin_index)

        return frame

    def start_video(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            frame = self.process_frame(frame)

            cv2.imshow('Makeup Application', frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    makeup_app = MakeupApplication()
    makeup_app.start_video()
