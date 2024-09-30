import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt

# 4. Load and Prepare Data
data = pd.read_csv('vehicle_anomaly_dataset.csv')
X = data[['gyro_x', 'gyro_y', 'gyro_z', 'pedometer', 'radar_distance', 'radar_velocity', 'potentiometer_angle']]
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Train Isolation Forest
iso_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
X_train_normal = X_train[y_train == 0]
iso_forest.fit(scaler.transform(X_train_normal))
y_pred = iso_forest.predict(X_test_scaled)
y_pred = np.where(y_pred == 1, 0, 1)

# 6. Evaluate Isolation Forest
print("Isolation Forest Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("ROC AUC Score:")
print(roc_auc_score(y_test, iso_forest.decision_function(X_test_scaled)))

# 7. Plot Reconstruction Error for Autoencoder
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

autoencoder = Sequential([
    Dense(4, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dense(X_train_scaled.shape[1], activation='sigmoid')
])
autoencoder.compile(optimizer=Adam(lr=0.001), loss='mse')
autoencoder.fit(X_train_normal, X_train_normal, epochs=50, batch_size=32, validation_split=0.1, shuffle=True)

X_test_pred = autoencoder.predict(X_test_scaled)
reconstruction_error = np.mean(np.abs(X_test_scaled - X_test_pred), axis=1)
threshold = np.percentile(reconstruction_error, 95)
y_pred_auto = (reconstruction_error > threshold).astype(int)

print("\nAutoencoder Classification Report:")
print(classification_report(y_test, y_pred_auto))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_auto))
print("ROC AUC Score:")
print(roc_auc_score(y_test, reconstruction_error))
