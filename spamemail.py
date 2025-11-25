import pickle
import numpy as np
import pandas as pd
import seaborn as sns
from django.contrib.staticfiles.storage import staticfiles_storage

sns.set_style("white")
import matplotlib.pyplot as plt
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import nltk
from nltk.corpus import stopwords
import os
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
# nltk.download('stopwords')


def process(text):
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    clean = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    return clean


def validate(body):
    vectorizer_path = 'static/models/vectorizer.pkl'
    model_path = 'static/models/model.pkl'
    os.makedirs('static/models', exist_ok=True)

    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print("Training model...")

        dataset = pd.read_csv(staticfiles_storage.path('dataset/emails_short.csv'))
        dataset.drop_duplicates(inplace=True)

        vect = CountVectorizer(analyzer=process)
        message = vect.fit_transform(dataset['text'])

        X_train, X_test, y_train, y_test = train_test_split(message, dataset['spam'], test_size=0.20, random_state=0)

        model = MultinomialNB()
        model.fit(X_train, y_train)

        # Save the model and vectorizer
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(vect, f)
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

        print("Model trained with accuracy:", accuracy_score(y_test, model.predict(X_test)) * 100)

    else:
        # Load model and vectorizer
        with open(vectorizer_path, 'rb') as f:
            vect = pickle.load(f)
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

    input_data = vect.transform([body])
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        return "Spam"
    else:
        return"Not Spam"