import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from tensorflow.keras.preprocessing.sequence import pad_sequences


class KeywordSpotter:
    def __init__(self, max_sequence_length=20, embedding_dim=50):
        self.max_sequence_length = max_sequence_length
        self.embedding_dim = embedding_dim
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential([
            Input(shape=(self.max_sequence_length, self.embedding_dim)),
            LSTM(64, return_sequences=True),
            LSTM(32),
            Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train(self, X, y, epochs=10, batch_size=32):
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size)

    def predict(self, X):
        return self.model.predict(X)

    def preprocess_text(self, text):
        # Simple character-level embedding
        return np.array([[ord(c) / 255.0 for c in text]])

    def pad_sequence(self, sequence):
        return pad_sequences(sequence, maxlen=self.max_sequence_length, padding='post', truncating='post')

# Example usage
if __name__ == "__main__":
    spotter = KeywordSpotter()
    
    # Example training data
    X_train = np.random.rand(100, 20, 50)  # 100 samples, 20 timesteps, 50 features
    y_train = np.random.randint(0, 2, 100)  # Binary labels
    
    # Pad sequences to the maximum length
    X_train = spotter.pad_sequence(X_train)
    
    spotter.train(X_train, y_train)
    
    # Example prediction
    X_test = np.random.rand(1, 20, 50)
    X_test = spotter.pad_sequence(X_test)
    prediction = spotter.predict(X_test)
    print(f"Prediction: {prediction[0][0]}")