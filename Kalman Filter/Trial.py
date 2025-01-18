import numpy as np

# Initialize variables
dt = 1  # Time step
x = 0  # Initial position estimate
P = 1  # Initial estimation error covariance
A = 1  # State transition matrix
H = 1  # Measurement matrix
Q = 0.01  # Process noise covariance
R = 0.1  # Measurement noise covariance

# Kalman Filter equations
def kalman_filter(z, x, P):
    # Predict step
    x_pred = A * x
    P_pred = A * P * A + Q

    # Update step
    K = P_pred * H / (H * P_pred * H + R)  # Kalman gain
    x_upd = x_pred + K * (z - H * x_pred)  # Update estimate
    P_upd = (1 - K * H) * P_pred          # Update error covariance

    return x_upd, P_upd

# Simulate noisy measurements
true_values = [5 + i for i in range(50)]  # True values (linearly increasing position)
measurements = [v + np.random.normal(0, 0.5) for v in true_values]  # Noisy observations

# Apply Kalman Filter
filtered_values = []
for z in measurements:
    x, P = kalman_filter(z, x, P)
    filtered_values.append(x)

# Plot results
import matplotlib.pyplot as plt

plt.plot(true_values, label="True Values", linestyle="--", color="black")
plt.plot(measurements, label="Measurements", marker="o", color="red", linestyle="none")
plt.plot(filtered_values, label="Kalman Filter Output", color="blue")
plt.legend()
plt.xlabel("Time")
plt.ylabel("Position")
plt.title("Simple Kalman Filter")
plt.show()