from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from textblob import TextBlob

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    message = data['message']
    blob = TextBlob(message)

    # Get the polarity and subjectivity
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Classify sentiment
    if polarity > 0:
        sentiment = 'positive'
    elif polarity < 0:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    response = {
        'message': f"Sentiment: {sentiment} (Polarity: {polarity:.2f}, Subjectivity: {subjectivity:.2f})"
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
