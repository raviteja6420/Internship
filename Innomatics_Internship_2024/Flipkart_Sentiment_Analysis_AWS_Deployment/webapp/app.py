from flask import Flask, render_template, request
import joblib
import re

app = Flask(__name__)

# Load the saved best model
best_model = joblib.load('svm_model.pkl')

# Function to preprocess the input text
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove special characters, punctuation, and extra whitespaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the input review from the form
        review = request.form['review']
        # Preprocess the input review
        processed_review = preprocess_text(review)
        # Use the best model to predict the sentiment
        prediction = best_model.predict([processed_review])[0]
        # Map prediction to sentiment label
        sentiment = "Positive" if prediction == 'Positive' else "Negative"
        return render_template('result.html', sentiment=sentiment, review=review)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
