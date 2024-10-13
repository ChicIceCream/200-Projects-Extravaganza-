from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import itertools
import numpy as np

app = Flask(__name__)

# Class for applying virtual makeup using OpenCV and MediaPipe
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

    # ... (include all the methods from the original MakeupApplication class)

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

        return frame

# Initialize makeup application class
makeup_app = MakeupApplication()

# Initialize the camera
camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            processed_frame = makeup_app.process_frame(frame)
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)