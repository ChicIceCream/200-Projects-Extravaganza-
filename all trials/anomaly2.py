import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# Define the number of samples
num_samples = 20000

# Define the percentage of anomalies
anomaly_percentage = 0.01  # 1%
num_anomalies = int(num_samples * anomaly_percentage)

# Generate timestamps (assuming one reading per second)
timestamps = pd.date_range(start='2024-01-01', periods=num_samples, freq='S')

# Generate normal sensor data using realistic distributions
# Gyroscope readings (degrees/s)
gyro_x = np.random.normal(loc=0, scale=1, size=num_samples)
gyro_y = np.random.normal(loc=0, scale=1, size=num_samples)
gyro_z = np.random.normal(loc=0, scale=1, size=num_samples)

# Pedometer readings (steps/min)
pedometer = np.random.normal(loc=50, scale=10, size=num_samples)

# Radar readings
radar_distance = np.random.normal(loc=30, scale=5, size=num_samples)  # meters
radar_velocity = np.random.normal(loc=0, scale=2, size=num_samples)  # m/s

# Potentiometer readings (steering angle in degrees)
potentiometer_angle = np.random.normal(loc=0, scale=5, size=num_samples)

# Create DataFrame
data = pd.DataFrame({
    'timestamp': timestamps,
    'gyro_x': gyro_x,
    'gyro_y': gyro_y,
    'gyro_z': gyro_z,
    'pedometer': pedometer,
    'radar_distance': radar_distance,
    'radar_velocity': radar_velocity,
    'potentiometer_angle': potentiometer_angle,
    'label': 0  # Initialize all as normal
})

# Display first few rows
print("Initial Data Sample:")
print(data.head())

# -------------------------
# Inject Anomalies
# -------------------------

# Randomly choose indices for anomalies
anomaly_indices = np.random.choice(data.index, size=num_anomalies, replace=False)

# Inject anomalies in selected indices

# 1. Gyroscope spikes (sudden high angular velocity)
gyro_spike_factor = 20
gyro_spike_std = 5
data.loc[anomaly_indices, 'gyro_x'] += np.random.normal(loc=gyro_spike_factor, scale=gyro_spike_std, size=num_anomalies)
data.loc[anomaly_indices, 'gyro_y'] += np.random.normal(loc=gyro_spike_factor, scale=gyro_spike_std, size=num_anomalies)
data.loc[anomaly_indices, 'gyro_z'] += np.random.normal(loc=gyro_spike_factor, scale=gyro_spike_std, size=num_anomalies)

# 2. Pedometer anomalies (sudden high movement)
pedometer_anomaly_factor = 100
pedometer_anomaly_std = 20
data.loc[anomaly_indices, 'pedometer'] += np.random.normal(loc=pedometer_anomaly_factor, scale=pedometer_anomaly_std, size=num_anomalies)

# 3. Radar distance anomalies (objects too close)
radar_distance_anomaly_shift = -25  # Objects suddenly much closer
radar_distance_anomaly_std = 5
data.loc[anomaly_indices, 'radar_distance'] += np.random.normal(loc=radar_distance_anomaly_shift, scale=radar_distance_anomaly_std, size=num_anomalies)

# 4. Radar velocity anomalies (objects approaching too fast)
radar_velocity_anomaly_factor = 20
radar_velocity_anomaly_std = 5
data.loc[anomaly_indices, 'radar_velocity'] += np.random.normal(loc=radar_velocity_anomaly_factor, scale=radar_velocity_anomaly_std, size=num_anomalies)

# 5. Potentiometer angle anomalies (sharp turns)
potentiometer_angle_anomaly_factor = 45
potentiometer_angle_anomaly_std = 10
data.loc[anomaly_indices, 'potentiometer_angle'] += np.random.normal(loc=potentiometer_angle_anomaly_factor, scale=potentiometer_angle_anomaly_std, size=num_anomalies)

# Label anomalies
data.loc[anomaly_indices, 'label'] = 1

# Shuffle the dataset to mix anomalies with normal data
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

# Verify the number of anomalies
print(f"\nTotal Samples: {len(data)}")
print(f"Total Anomalies Injected: {data['label'].sum()}")

# Save the dataset to a CSV file
output_filename = 'vehicle_anomaly_dataset_20000.csv'
data.to_csv(output_filename, index=False)
print(f"\nSynthetic dataset with {len(data)} samples created and saved to '{output_filename}'.")

# Optional: Visualize the distribution of labels
# import seaborn as sns

# plt.figure(figsize=(6,4))
# sns.countplot(x='label', data=data)
# plt.title('Distribution of Normal and Anomalous Samples')
# plt.xlabel('Label (0: Normal, 1: Anomaly)')
# plt.ylabel('Count')
# plt.show()
