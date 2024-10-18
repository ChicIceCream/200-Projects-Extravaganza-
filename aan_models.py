import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf

# Load the data
data = pd.read_csv('all trials\\ANN MAAM\\ANN_data.csv')

# Assuming the last column is the threshold voltage
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

# MLP
mlp_model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42)
mlp_model.fit(X_train_scaled, y_train)

# ANN (using TensorFlow)
ann_model = tf.keras.Sequential([
    tf.keras.layers.Dense(100, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    tf.keras.layers.Dense(50, activation='relu'),
    tf.keras.layers.Dense(1)
])
ann_model.compile(optimizer='adam', loss='mse')
ann_model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, verbose=0)

# Evaluate models
def evaluate_model(model, X, y, model_name):
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    print(f"{model_name} - MSE: {mse:.4f}, R2: {r2:.4f}")

evaluate_model(lr_model, X_test_scaled, y_test, "Linear Regression")
evaluate_model(mlp_model, X_test_scaled, y_test, "MLP")
evaluate_model(ann_model, X_test_scaled, y_test, "ANN")

# Generate equations for plotting
def lr_equation(X):
    return lr_model.intercept_ + np.dot(X, lr_model.coef_)

def mlp_equation(X):
    return mlp_model.predict(X)

def ann_equation(X):
    return ann_model.predict(X).flatten()

print("\nEquations for plotting:")
print("Linear Regression:")
print(f"y = {lr_model.intercept_:.4f}", end="")
for i, coef in enumerate(lr_model.coef_):
    print(f" + {coef:.4f} * x{i+1}", end="")
print()
print("MLP: Use mlp_equation(X) function")
print("ANN: Use ann_equation(X) function")

# Example of how to use these equations for plotting
import matplotlib.pyplot as plt

# Choose a feature to plot against (e.g., the first feature)
feature_index = 0
feature_name = X.columns[feature_index]

# Generate a range of values for the chosen feature
x_range = np.linspace(X.iloc[:, feature_index].min(), X.iloc[:, feature_index].max(), 100)

# Create input data for predictions
X_plot = pd.DataFrame(np.tile(X.mean().values, (100, 1)), columns=X.columns)
X_plot[feature_name] = x_range
X_plot_scaled = scaler.transform(X_plot)

# Generate predictions
y_lr = lr_equation(X_plot_scaled)
y_mlp = mlp_equation(X_plot_scaled)
y_ann = ann_equation(X_plot_scaled)

# Plot the results
plt.figure(figsize=(10, 6))
plt.scatter(X[feature_name], y, alpha=0.5, label='Data')
plt.plot(x_range, y_lr, label='Linear Regression', color='red')
plt.plot(x_range, y_mlp, label='MLP', color='green')
plt.plot(x_range, y_ann, label='ANN', color='blue')
plt.xlabel(feature_name)
plt.ylabel('Threshold Voltage')
plt.legend()
plt.title(f'Model Predictions vs {feature_name}')
plt.show()
