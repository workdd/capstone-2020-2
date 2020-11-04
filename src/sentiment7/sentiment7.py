# -*- coding: utf-8 -*-
import codecs

from konlpy.tag import Okt
okt = Okt()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import time
import joblib
import pickle
import numpy
def fitting(sample_labels, sample_text):
    test_start = int(len(sample_text)/5)*4

    test_text = sample_text[test_start:]
    test_labels = sample_labels[test_start:]
    train_text = sample_text[:test_start]
    train_labels = sample_labels[:test_start]

    test_text_ = [' '.join(word[0] for word in okt.pos(text, norm=True)) for text in test_text]

    trained_vectorizer = TfidfVectorizer(ngram_range=(1, 1))
    train_text_feat = trained_vectorizer.fit_transform(train_text)
    test_text_feat = trained_vectorizer.transform(test_text_)
    
    with open("vectorizer.pickle", "wb") as f:
        pickle.dump(trained_vectorizer, f)

    trained_clf = svm.SVC(kernel='linear').fit(train_text_feat, train_labels)

    joblib.dump(trained_clf, '7sentiment.model') 

    predicted = trained_clf.predict(test_text_feat)

    correct = 0
    for pred, label in zip(predicted, test_labels):
    	if pred == label:
    	    correct += 1

    acc = correct / len(test_labels)
    return acc

def predict_7sentiment(chat):
    with open("../sentiment7/vectorizer.pickle", "rb") as f:
        vectorizer = pickle.load(f)

    chat_feat = vectorizer.transform(chat)
    model = joblib.load('../sentiment7/7sentiment.model')
    return model.predict(chat_feat)

def counting(a):
    sentiment = ['joy', 'sadness', 'neutral', 'fear', 'love', 'surprise', 'anger']
    dic = {}
    for s in sentiment:
    	dic[s] = a.count(s)
    return dic
