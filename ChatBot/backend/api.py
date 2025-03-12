# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import webbrowser
import os
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize Flask app
app = Flask(__name__, static_folder="frontend", template_folder="frontend")
CORS(app)

# Define base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load trained components
try:
    model = pickle.load(open(os.path.join(BASE_DIR, "chatbot_model.pkl"), "rb"))
    vectorizer = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb"))
    tags = pickle.load(open(os.path.join(BASE_DIR, "tags.pkl"), "rb"))
    responses = pickle.load(open(os.path.join(BASE_DIR, "responses.pkl"), "rb"))
except FileNotFoundError as e:
    print(f"❌ Error loading model files: {e}")
    exit()

lemmatizer = WordNetLemmatizer()

# ✅ Serve Frontend
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# ✅ Chatbot API Endpoint
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    if not user_input:  # Handle empty input
        return jsonify({"error": "No message provided"}), 400

    # Preprocess user input
    words = [lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(user_input)]
    input_text = " ".join(words)

    # Convert input into vector form
    input_vector = vectorizer.transform([input_text])

    try:
        # Predict tag
        tag_index = model.predict(input_vector)[0]
        predicted_tag = tags[tag_index]

        # Get a response from the dictionary
        response = responses.get(predicted_tag, ["I don't understand."])[0]

        return jsonify({"response": response})  # ✅ Ensure return is inside the function

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500  # Handle errors

if __name__ == "__main__":
    print("🚀 Starting Flask server at http://127.0.0.1:5000")
    
    # Open browser automatically after backend starts
    webbrowser.open("http://127.0.0.1:5000")

    # Run Flask without reloader (prevents opening browser twice)
    app.run(port=5000, debug=True, use_reloader=False)
