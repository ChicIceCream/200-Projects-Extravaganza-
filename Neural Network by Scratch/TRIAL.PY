import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Load the data
data = pd.read_csv("Neural Network by Scratch/digit-recognizer/train.csv")

# Convert the data into a numpy array and shuffle it
data = np.array(data)
np.random.shuffle(data)  # shuffle the data

# Split the data into training and validation sets
data_val = data[:1000].T
Y_val = data_val[0]
X_val = data_val[1:]

data_train = data[1000:].T
Y_train = data_train[0]
X_train = data_train[1:]

# Normalize the data by scaling pixel values to the range 0-1
X_train = X_train / 255.0
X_val = X_val / 255.0

# Initialize weights and biases for the neural network
def initialize_parameters():
    W1 = np.random.randn(10, 784) * 0.01  # Small random values
    b1 = np.zeros((10, 1))
    W2 = np.random.randn(10, 10) * 0.01
    b2 = np.zeros((10, 1))
    return W1, b1, W2, b2

# Apply ReLU activation function
def relu_activation(Z):
    return np.maximum(Z, 0)

# Apply softmax activation function
def softmax_activation(Z):
    Z_shifted = Z - np.max(Z, axis=0, keepdims=True)
    exp_values = np.exp(Z_shifted)
    A = exp_values / np.sum(exp_values, axis=0, keepdims=True)
    return A

# Forward propagation
def forward_prop(W1, b1, W2, b2, X):
    Z1 = W1.dot(X) + b1
    A1 = relu_activation(Z1)
    Z2 = W2.dot(A1) + b2
    A2 = softmax_activation(Z2)
    return Z1, A1, Z2, A2

# ReLU derivative
def ReLU_deriv(Z):
    return Z > 0

# One-hot encoding for the labels
def one_hot(Y):
    one_hot_Y = np.zeros((Y.size, Y.max() + 1))
    one_hot_Y[np.arange(Y.size), Y] = 1
    return one_hot_Y.T

# Backward propagation
def backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y):
    m = X.shape[1]
    one_hot_Y = one_hot(Y)
    dZ2 = A2 - one_hot_Y
    dW2 = 1 / m * dZ2.dot(A1.T)
    db2 = 1 / m * np.sum(dZ2, axis=1, keepdims=True)
    dZ1 = W2.T.dot(dZ2) * ReLU_deriv(Z1)
    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = 1 / m * np.sum(dZ1, axis=1, keepdims=True)
    return dW1, db1, dW2, db2

# Update weights and biases
def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1
    W2 = W2 - alpha * dW2
    b2 = b2 - alpha * db2
    return W1, b1, W2, b2

# Get predictions
def get_predictions(A2):
    return np.argmax(A2, 0)

# Calculate accuracy
def get_accuracy(predictions, Y):
    return np.sum(predictions == Y) / Y.size

# Gradient descent training loop
def gradient_descent(X, Y, alpha, iterations):
    W1, b1, W2, b2 = initialize_parameters()
    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
        dW1, db1, dW2, db2 = backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y)
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
        if i % 100 == 0:
            print(f"Iteration: {i}")
            predictions = get_predictions(A2)
            accuracy = get_accuracy(predictions, Y)
            print(f"Accuracy: {accuracy}")
    return W1, b1, W2, b2

# Train the model
W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 0.10, 500)

# Make predictions
def make_predictions(X, W1, b1, W2, b2):
    _, _, _, A2 = forward_prop(W1, b1, W2, b2, X)
    predictions = get_predictions(A2)
    return predictions

# Test predictions
def test_prediction(index, W1, b1, W2, b2):
    current_image = X_train[:, index, None]
    prediction = make_predictions(current_image, W1, b1, W2, b2)
    label = Y_train[index]
    print(f"Prediction: {prediction}")
    print(f"Label: {label}")

    current_image = current_image.reshape((28, 28)) * 255
    plt.gray()
    plt.imshow(current_image, interpolation='nearest')
    plt.show()

# Test some predictions
test_prediction(0, W1, b1, W2, b2)
test_prediction(1, W1, b1, W2, b2)
test_prediction(2, W1, b1, W2, b2)
test_prediction(3, W1, b1, W2, b2)
