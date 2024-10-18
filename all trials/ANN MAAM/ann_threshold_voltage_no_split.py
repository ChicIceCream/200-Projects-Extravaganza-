
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Load the dataset
data = pd.read_csv('all trials\\ANN MAAM\\ANN_data.csv')

# Data Preprocessing
# Dropping rows with NaN values for simplicity
data_cleaned = data.dropna()

# Selecting the input features (all numeric columns except the target)
X = data_cleaned.iloc[:, 1:-1].values  # assuming all except last column are input features
y = data_cleaned.iloc[:, -1].values    # assuming last column is the target (threshold voltage)

# Feature scaling
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Build the ANN model
model = Sequential()

# Input layer and first hidden layer
model.add(Dense(units=64, activation='relu', input_dim=X.shape[1]))

# Adding second hidden layer
model.add(Dense(units=32, activation='relu'))

# Output layer (single value prediction)
model.add(Dense(units=1, activation='linear'))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model on the entire dataset (no train-test split)
model.fit(X, y, epochs=50, batch_size=10, verbose=1)

# Predict the threshold voltage for the full dataset
y_pred = model.predict(X)

# Save the model for future use
model.save('ann_model_threshold_voltage_full_data.h5')
