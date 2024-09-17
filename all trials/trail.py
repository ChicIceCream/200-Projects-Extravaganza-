import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Step 1: Data Preparation (assuming you have a CSV with question ids, responses, and class labels)
# Example structure: 'question_id', 'response', 'class_label'
data = {
    'question_id': [1, 2, 3, 4, 5],
    'response': [1, 0, 1, 0, 1],
    'class_label': ['A', 'B', 'A', 'B', 'A']
}

df = pd.DataFrame(data)

# Step 2: Feature Encoding (question_id and response as input, class_label as target)
X = df[['question_id', 'response']]
y = df['class_label']

# Step 3: Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Initialize the model
model = LogisticRegression()

# Step 5: Train the model
model.fit(X_train, y_train)

# Step 6: Make predictions
y_pred = model.predict(X_test)

# Step 7: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Step 8: Prediction for a new user response
new_user = np.array([[6, 1]])  # New question_id and response
predicted_class = model.predict(new_user)
print(f'Predicted class for new user: {predicted_class[0]}')
