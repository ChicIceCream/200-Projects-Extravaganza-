import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('all trials\\ANN MAAM\\ANN_data.csv')

# Prepare the features and target
features = ['Al_mole_fraction', 'In_Mole_fraction', 'Drain_Voltage_Vd', 'Vg', 'Id']
X = data[features]
y = data['Threshold_Voltage_Vth']

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create and train the MLP model
mlp = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42)
mlp.fit(X_scaled, y)

# Create and train the ANN model (using another MLP with different parameters)
ann = MLPRegressor(hidden_layer_sizes=(50, 25), max_iter=1000, random_state=42)
ann.fit(X_scaled, y)

# Function to get equation string for a model
def get_equation(model, feature_names, scaler):
    eq = "Threshold_Voltage_Vth = "
    for layer_idx, layer in enumerate(model.coefs_):
        if layer_idx == 0:
            for neuron_idx, neuron in enumerate(layer.T):
                eq += f"f{layer_idx+1}_{neuron_idx+1}("
                for feat_idx, feat in enumerate(neuron):
                    scale = scaler.scale_[feat_idx]
                    mean = scaler.mean_[feat_idx]
                    eq += f"{feat:.4f} * ({feature_names[feat_idx]} - {mean:.4f}) / {scale:.4f} + "
                eq = eq[:-3] + ") + "
        else:
            for neuron_idx, neuron in enumerate(layer.T):
                eq += f"f{layer_idx+1}_{neuron_idx+1}("
                for prev_neuron_idx, weight in enumerate(neuron):
                    eq += f"{weight:.4f} * f{layer_idx}_{prev_neuron_idx+1} + "
                eq = eq[:-3] + ") + "
    eq = eq[:-3]
    return eq

# Get equations
mlp_eq = get_equation(mlp, features, scaler)
ann_eq = get_equation(ann, features, scaler)

print("MLP Equation:")
print(mlp_eq)
print("\nANN Equation:")
print(ann_eq)

# Create a plot of actual vs predicted values
y_pred_mlp = mlp.predict(X_scaled)
y_pred_ann = ann.predict(X_scaled)

plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred_mlp, color='blue', label='MLP')
plt.scatter(y, y_pred_ann, color='red', label='ANN')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Actual Threshold Voltage')
plt.ylabel('Predicted Threshold Voltage')
plt.title('ANN and MLP Predictions vs Actual Threshold Voltage (Full Data Fit)')
plt.legend()
plt.grid(True)
plt.show()

# Print feature importances (for MLP, as an example)
importances = np.abs(mlp.coefs_[0]).sum(axis=1)
feature_importance = pd.DataFrame({'feature': features, 'importance': importances})
print("\nFeature Importances (MLP):")
print(feature_importance.sort_values('importance', ascending=False))