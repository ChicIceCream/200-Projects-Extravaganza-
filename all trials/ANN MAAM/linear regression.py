import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('all trials\\ANN MAAM\\ANN_data.csv')

# Prepare the features and target
features = ['Al_mole_fraction', 'In_Mole_fraction', 'Drain_Voltage_Vd', 'Vg', 'Id']
X = data[features]
y = data['Threshold_Voltage_Vth']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and fit the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Get the equation coefficients
coefficients = model.coef_
intercept = model.intercept_

# Create the equation string
equation = f"Threshold_Voltage_Vth = {intercept:.4f}"
for feature, coef in zip(features, coefficients):
    equation += f" + {coef:.4f} * {feature}"

print("Linear Regression Equation:")
print(equation)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate R-squared score and MSE for the test set
r_squared = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"\nTest Set Results:")
print(f"R-squared score: {r_squared:.4f}")
print(f"Mean Squared Error: {mse:.4f}")

# Plot actual vs predicted values for the test set
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Threshold Voltage')
plt.ylabel('Predicted Threshold Voltage')
plt.title('Linear Regression: Predicted vs Actual Threshold Voltage (Test Set)')
plt.grid(True)
plt.show()

# Print feature importances
importances = pd.DataFrame({'feature': features, 'importance': np.abs(coefficients)})
print("\nFeature Importances:")
print(importances.sort_values('importance', ascending=False))