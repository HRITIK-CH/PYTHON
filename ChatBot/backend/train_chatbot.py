# -*- coding: utf-8 -*-
import json
import nltk
import numpy as np
import pickle
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC

# Download required NLTK resources
nltk.download("punkt")
nltk.download("wordnet")

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# ✅ Load dataset correctly
try:
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)  # ✅ Ensure "data" is defined properly
except FileNotFoundError:
    print("❌ Error: 'data.json' not found. Make sure the file exists in the correct directory.")
    exit()

# Prepare training data
tags = []
patterns = []
responses = {}

for intent in data["intents"]:  # ✅ Now "data" is properly defined
    tag = intent["tag"]
    tags.append(tag)
    responses[tag] = intent["responses"]

    for pattern in intent["patterns"]:
        patterns.append(pattern)

# Tokenize and preprocess text
corpus = []
for pattern in patterns:
    words = nltk.word_tokenize(pattern)
    words = [lemmatizer.lemmatize(word.lower()) for word in words]
    corpus.append(" ".join(words))

# Convert text to numerical vectors
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)

# Create labels (convert tags to numbers)
y = []
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        y.append(intent["tag"])

# Convert labels to numerical format
y = np.array([tags.index(label) for label in y])

# Train SVM model
model = LinearSVC()
model.fit(X, y)

# Save trained model and vectorizer
pickle.dump(model, open("chatbot_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
pickle.dump(tags, open("tags.pkl", "wb"))
pickle.dump(responses, open("responses.pkl", "wb"))

print("✅ Chatbot model trained successfully!")
