import numpy as np
import cv2 
import tkinter as tk

# We will track 2 state variables (position and velocity)
# and one measurement variable (position)
kalman = cv2.KalmanFilter(2, 1)

# State transition matrix (A):
kalman.transitionMatrix = np.array([[1., 1.], [0., 1.]], dtype=np.float32)

# Measurement Matrix (H):
kalman.measurementMatrix = np.array([[1., 0.]], dtype=np.float32)

# Process Noise Convariance (Q):
kalman.processNoiseCov = np.array([[1., 0.], [0., 1.]], dtype=np.float32) * 0.0001

# Measurement Noise Covariance (R):
kalman.measurementNoiseCov = np.array([[1.]], dtype=np.float32) * 0.001

# Initialising the state
kalman.statePost = np.array([[0.], [0.]], dtype=np.float32)

# ----- Tkinter Setup ----- #
root = tk.Tk()
root.title("1D Kalman Filter Demo")
canvas_width = 800
canvas_height = 200
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")

canvas.pack(pady=20)

# Updating the filter
def update_filter(slider_value_str):
    """ This function is called every time the slider moves """

    #* 1. Predict step
    predicted_state = kalman.predict()

    #* 2. Get the measurement from the slider
    measurement_val = float(slider_value_str)
    measurement = np.array([[measurement_val]], dtype=np.float32)

    #* 3. Correction/Update step
    kalman.correct(measurement)

    # get the corrected state for visualisation
    corrected_state = kalman.statePost

    # ---- Visualisation ---- #
    canvas.delete("all")

    # A. Draw the raw measurement (from slider)
    raw_pos = measurement_val
    canvas.create_rectangle(raw_pos - 5, 50, raw_pos + 5, 70, fill="red", outline="red")
    canvas.create_text(raw_pos, 85, text="Measured", fill="red")
    
    # B. Draw the Kalman Filter's estimated position
    filtered_pos = corrected_state[0, 0]
    canvas.create_rectangle(filtered_pos - 5, 120, filtered_pos + 5, 140, fill="blue", outline="blue")
    canvas.create_text(filtered_pos, 155, text="Kalman Filtered", fill="blue")

    # C. Display the estimated velocity
    estimated_velocity = corrected_state[1, 0]
    canvas.create_text(canvas_width / 2, 20, 
                        text=f"Estimated Velocity: {estimated_velocity:.2f} pixels/update", 
                        font=("Arial", 12))


# --- Create the Slider Widget ---
slider = tk.Scale(root, from_=0, to=canvas_width - 10, orient="horizontal", 
                length=canvas_width, command=update_filter)
slider.pack(padx=20, pady=10)


# Initialize the canvas with the starting position
update_filter("0")

# Start the Tkinter event loop
root.mainloop()

