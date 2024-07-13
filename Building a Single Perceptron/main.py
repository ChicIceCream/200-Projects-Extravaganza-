'''
An approach to create a single perceptron using Python.
'''

inputs = [1, 2, 3, 4, 5]
targets = [3, 6, 9, 12, 15]

# This is similar to the Linear Regression algorithm, but with a single perceptron

# We know the function that we need to write the weights is : y = mx + c
# Right now, c = 0 and the equation is : y = 3x

w = 0.1 # Random weight

def predict(i):
    return w * i

prediction = [predict(i) for i in inputs]


# print(f'Prediction : {prediction}') # This output is pretty much random
# Rest is done in google colab