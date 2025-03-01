from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)  

# Load the pre-trained sentiment model and vectorizer
model = joblib.load('sentiment_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')  # Ensure you have a vectorizer

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    message = data['message']
    
    # Preprocess the message using the vectorizer
    message_vectorized = vectorizer.transform([message])
    
    # Predict sentiment based on the vectorized message
    sentiment = model.predict(message_vectorized)[0]
    
    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}

    # Assuming sentiment is predicted as one of 'positive', 'neutral', or 'negative'
    if sentiment in sentiment_counts:
        sentiment_counts[sentiment] += 1

    total_words = len(message.split())
    if total_words == 0:
        return jsonify({'message': "No words to analyze."})

    sentiment_percentages = {k: (v / total_words) * 100 for k, v in sentiment_counts.items() if v > 0}

    if not any(sentiment_counts.values()):
        return jsonify({'message': "No sentiments found in the text."})

    most_common_sentiment = max(sentiment_counts, key=sentiment_counts.get) if any(sentiment_counts.values()) else 'undefined'
    most_common_percentage = sentiment_percentages.get(most_common_sentiment, 0)

    response = {
        'message': f"Most common sentiment: {most_common_sentiment} ({most_common_percentage:.2f}%)",
        'details': sentiment_percentages
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
