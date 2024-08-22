import pandas as pd
import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression

# Read the data from a CSV file
data2 = pd.read_csv("Algorithms from Scratch\Linear Regression\data2.csv")

# Function to calculate the total error for a given line (slope and intercept)
def loss_function(m, c, points):
    total_error = 0
    for i in range(len(points)):
        x = points.iloc[i].X
        y = points.iloc[i].Y
        total_error += (y - (m * x + c)) ** 2  # Squared error for each point
    return total_error / float(len(points))  # Average squared error

# Function to calculate the gradients for slope and intercept
def gradient_descent(m_now, c_now, points, L):
    m_gradient = points.iloc[len(points) // 2].X  # Initial value for slope gradient
    c_gradient = points.iloc[len(points) // 2].Y  # Initial value for intercept gradient
    n = len(points)
    for i in range(n):
        x = points.iloc[i].X
        y = points.iloc[i].Y
        m_gradient += -(2 / n) * x * (y - (m_now * x + c_now))  # Update slope gradient
        c_gradient += -(2 / n) * (y - (m_now * x + c_now))  # Update intercept gradient
    m = m_now - m_gradient * L  # Update slope with learning rate
    c = c_now - c_gradient * L  # Update intercept with learning rate
    return m, c

# Initialize slope, intercept, and learning rate
m, c, L = 0, 0, 0.0001
epochs = 1000  # Number of iterations

# Gradient Descent algorithm
for i in range(epochs):
    m, c = gradient_descent(m, c, data2, L)
    if epochs % 100 == 0:
        print(f'Epochs = {i}')
        print(m, c)

# Plot the data and the best-fit line
plt.scatter(data2.X, data2.Y, color='black')
plt.plot(list(range(0, 30)), [m * x + c for x in range(0, 30)], color='red')
plt.show()