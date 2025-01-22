import numpy as np
import matplotlib.pyplot as plt

class KalmanFilter1D:
    """
    A simple 1D Kalman Filter implementation for tracking position and velocity
    of an object moving in one dimension.
    """
    
    def __init__(self, initial_position, position_uncertainty):
        # State vector [position, velocity]
        self.state = np.array([initial_position, 0.0])
        
        # Covariance matrix P
        # Represents uncertainty in the state estimate
        # [[position_variance, position_velocity_covariance],
        #  [position_velocity_covariance, velocity_variance]]
        self.P = np.array([[position_uncertainty, 0],
                            [0, 1000.0]])  # High initial velocity uncertainty
        
        # State transition matrix F
        # Defines how the state evolves over time
        # For constant velocity model:
        # new_position = old_position + velocity * dt
        # new_velocity = old_velocity
        self.dt = 0.1  # Time step                  ### Can change
        self.F = np.array([[1, self.dt],1
                            [0, 1]])
        
        # Process noise covariance matrix Q
        # Represents uncertainty in the prediction step
        # Larger values mean we trust our predictions less
        process_noise = 0.1
        self.Q = process_noise * np.array([[self.dt**4/4, self.dt**3/2],
                                            [self.dt**3/2, self.dt**2]])
        
        # Measurement matrix H
        # Maps the state vector to measurement space
        # We only measure position, not velocity
        self.H = np.array([[1, 0]])
        
        # Measurement noise covariance R
        # Represents uncertainty in our measurements
        # Larger values mean we trust measurements less
        self.R = np.array([[1.0]])

    def predict(self):
        """
        Prediction step of the Kalman filter.
        Estimates the current state based on previous state.
        """
        # Project state ahead using state transition matrix
        self.state = np.dot(self.F, self.state)
        
        # Project covariance ahead
        # P = F * P * F_transpose + Q
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

    def update(self, measurement):
        """
        Update step of the Kalman filter.
        Corrects the state estimate using the measurement.
        
        Args:
            measurement: The observed position
        """
        # Calculate Kalman gain
        # K = P * H_transpose * inv(H * P * H_transpose + R)
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        
        # Update state estimate with measurement
        measurement_residual = measurement - np.dot(self.H, self.state)
        self.state = self.state + np.dot(K, measurement_residual)
        
        # Update covariance matrix
        # P = (I - K * H) * P
        I = np.eye(self.state.shape[0])
        self.P = np.dot((I - np.dot(K, self.H)), self.P)

def simulate_system():
    """
    Simulate a moving object and track it with the Kalman filter.
    """
    # True initial state (position = 0, velocity = 5)
    true_state = np.array([0.0, 5.0])
    
    # Create Kalman filter instance
    # Start with position=0 and high uncertainty
    kf = KalmanFilter1D(0.0, 1000.0)
    
    # Arrays to store data for plotting
    times = np.arange(0, 10, kf.dt)
    true_positions = []
    measured_positions = []
    estimated_positions = []
    
    # Simulation loop
    for t in times:
        # Update true state (constant velocity motion)
        true_state = np.dot(kf.F, true_state)
        true_position = true_state[0]
        
        # Generate noisy measurement
        measurement = true_position + np.random.normal(0, 1.0)
        
        # Kalman filter steps
        kf.predict()
        kf.update(measurement)
        
        # Store data for plotting
        true_positions.append(true_position)
        measured_positions.append(measurement)
        estimated_positions.append(kf.state[0])
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(times, true_positions, 'g-', label='True Position')
    plt.plot(times, measured_positions, 'r.', label='Measurements')
    plt.plot(times, estimated_positions, 'b-', label='Kalman Filter Estimate')
    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.title('1D Kalman Filter Tracking')
    plt.legend()
    plt.grid(True)
    plt.show()

# Run simulation
simulate_system()