import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# Load the data
data = pd.read_csv('ANN MAAM\\ANN_data.csv')  # Replace with actual file path

# Define input features (X) and output (y)
X = data[['Thickness', 'Al_Mole_Fraction', 'In_Mole_Fraction', 'Vd', 'Vg']]
y = data['Id']

# Fit a polynomial ridge regression model (degree 2 for non-linearity)
degree = 2  # Adjust as necessary
alpha_value = 0.1  # Adjust alpha for regularization strength
poly_ridge_model = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=alpha_value))

# Train the model
poly_ridge_model.fit(X, y)

# Predict Id based on the input features
y_pred = poly_ridge_model.predict(X)

# Print coefficients (for a human-readable equation)
print("Coefficients:", poly_ridge_model.named_steps['ridge'].coef_)
print("Intercept:", poly_ridge_model.named_steps['ridge'].intercept_)
