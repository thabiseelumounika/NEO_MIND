# train_chatbot.py

import json
import random
import pickle
import nltk
import os

from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB

# 📥 Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# 🔧 Initialize
lemmatizer = WordNetLemmatizer()
corpus = []
labels = []

# ✅ Load intents
with open('assistant/intents.json', encoding='utf-8') as file:
    intents = json.load(file)

# 🔄 Prepare corpus and labels
for intent in intents['intents']:
    for pattern in intent['patterns']:
        tokens = nltk.word_tokenize(pattern)
        tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens]
        corpus.append(" ".join(tokens))
        labels.append(intent['tag'])

# 🧠 Convert text to features
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)

# 🔍 Train model
model = MultinomialNB()
model.fit(X, y)

# 💾 Create model folder if it doesn't exist
os.makedirs("model", exist_ok=True)

# 💾 Save model and encoders
pickle.dump(model, open('model/chatbot_model.pkl', 'wb'))
pickle.dump(vectorizer, open('model/vectorizer.pkl', 'wb'))
pickle.dump(label_encoder, open('model/label_encoder.pkl', 'wb'))

print("✅ Model trained and saved successfully without TensorFlow.")
