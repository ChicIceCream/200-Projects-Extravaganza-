from flask import Flask, render_template, request, jsonify
from model import KeywordSpotter
import numpy as np

app = Flask(__name__)
spotter = KeywordSpotter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train():
    data = request.json
    keywords = data['keywords']
    non_keywords = data['non_keywords']
    
    X = []
    y = []
    
    for keyword in keywords:
        X.append(spotter.preprocess_text(keyword))
        y.append(1)
    
    for non_keyword in non_keywords:
        X.append(spotter.preprocess_text(non_keyword))
        y.append(0)
    
    X = np.vstack(X)
    X = spotter.pad_sequence(X)
    y = np.array(y)
    
    spotter.train(X, y)
    
    return jsonify({"message": "Model trained successfully"})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data['text']
    
    X = spotter.preprocess_text(text)
    X = spotter.pad_sequence(X)
    
    prediction = spotter.predict(X)[0][0]
    
    return jsonify({"prediction": float(prediction)})

if __name__ == '__main__':
    app.run(debug=True)