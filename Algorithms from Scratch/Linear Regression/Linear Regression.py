import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression 



# data = pd.read_csv("data.csv")
data2 = pd.read_csv("Linear Regression\data2.csv")
# print(data)

# plt.scatter(data2.X, data2.Y)
# plt.show()

def loss_function(m, c, points):
    total_error = 0
    for i in  range(len(points)):
        x = points.iloc[i].X
        y = points.iloc[i].Y        
        total_error += (y - ( m * x * c)) ** 2
    total_error / float(len(points))

def gradient_descent(m_now, c_now, points, L):
    m_gradient = points.iloc[len(points)//2].X
    c_gradient = points.iloc[len(points)//2].Y
    
    n = len(points)
    
    for i in range(n):
        x = points.iloc[i].X
        y = points.iloc[i].Y
        
        m_gradient += -(2/n) * x * (y - (m_now * x + c_now))
        c_gradient += -(2/n) * (y - (m_now * x + c_now))
    
    m = m_now - m_gradient * L
    c = c_now - c_gradient * L
    
    return m, c

m, c, L = 0, 0, 0.0001
epochs = 1000

for i in range(epochs):
    m, c = gradient_descent(m, c, data2, L)
    
    if epochs % 100 == 0:
        print(f'Epochs = {i}')


print(m, c)
plt.scatter(data2.X, data2.Y, color='black')
plt.plot(list(range(0, 30)), [m * x + c for x in range(0, 30)], color='red')
plt.show()