from flask_api import FlaskAPI
from flask import request, jsonify
from flask_cors import CORS
import pandas as pd
import csv
import numpy as np
from numpy import array
from sklearn import preprocessing
from pprint import pprint
from tensorflow.keras.models import load_model
import tensorflow as tf
import spacy
import nltk
from nltk.stem import PorterStemmer
import warnings
warnings.simplefilter('ignore')
ps = PorterStemmer()
nlp = spacy.load('en_core_web_sm')
# from autoencoder import X_train


def get_dict():
    synonym_dict = {}
    synonym_dict[('United States', 'USA', 'America',
                  'United States of America',)] = 'US'
    synonym_dict[('International student',
                  'international students')] = 'F1 student'
    synonym_dict[('San Jose State University', 'SJ State University')] = 'SJSU'
    synonym_dict[('International cell',
                  'International student and scholar services ')] = 'ISSS'
    synonym_dict[('Graduate admission and programs evaluation',
                  'Graduate admissions and program evaluation',)] = 'GAPE'
    synonym_dict[('Masters of Science in Software Engineering',
                  'MS in Software Engineering')] = 'MSSE'
    synonym_dict[('MS-ISE', 'MS ISE', 'Masters in Industrial and Systems Engineering',
                  'MS in Industrial and Systems Engineering', 'Masters in ISE', 'MS in ISE')] = 'MSISE'
    synonym_dict[('Computer Engineering', 'Computers Engineering')] = 'CMPE'
    synonym_dict[('Software Engineering', 'SW Engineering')] = 'SE'
    synonym_dict[('General Education', 'general education')] = 'GE'
    synonym_dict[('Writing skills test', 'Writing skill test')] = 'WST'
    synonym_dict[('lower division', 'lower-division')] = 'LD'
    synonym_dict[('California state university',
                  'CA state university')] = 'CSU'
    synonym_dict[('Former Student Returning',
                  'former student returning')] = 'FSR'
    synonym_dict[('Grade point average', 'grade point avg')] = 'GPA'
    synonym_dict[('Open University', 'open uni')] = 'OU'
    synonym_dict[('full-time', 'fulltime')] = 'full time'
    synonym_dict[('Free Application for Federal Student Aid',
                  'Free Application for Federal Students Aid')] = 'FAFSA'
    synonym_dict[('MS in Computer Science', 'Masters in CS',
                  'Masters in Computer Science', 'MS in CS')] = 'MSCS'
    synonym_dict[('part-time', 'parttime')] = 'part time'
    synonym_dict[('Child and Adolescent Development',
                  'child and adolescent development')] = 'ChAD'
    synonym_dict[('credit/no-credit', 'credit no-credit')] = 'CR/NCR'
    synonym_dict[('last day','deadline')] = 'deadline'
    return synonym_dict


def get_stopWords():
    stopwords = ["is", "an", "the", "are", "am",
                 "was", "were", "I", "we", "will", "would", "a"]
    return stopwords


def normalize_string(string):
    nlp = spacy.load('en_core_web_sm')
    test_string = ""
    # test_string = test_string.strip()
    for word in string:
        test_string += word.text.lower()
        test_string += " "

    synonym_dict = get_dict()

    for key in synonym_dict:
        for t in key:
            strng = t.lower()
            if strng in test_string:
                test_string = test_string.replace(strng, synonym_dict[key])

    return nlp(test_string)


def preprocess(sentence_1):
    s1_stem = ""
    stopwords = get_stopWords()
    for word in sentence_1:
        if word.text in stopwords:
            continue

        rootWord = ps.stem(str(word.text))
        s1_stem += rootWord
        s1_stem += " "

    return s1_stem




def create_app():
    app = FlaskAPI(__name__, instance_relative_config=True)

    CORS(app)

    @app.route('/nlp-normalize/', methods=['POST'])
    def ask():
        if request.method == "POST":
            sentence = str(request.data.get('question'))
            print("=======> Before normalizing : ",sentence)

            nlp = spacy.load('en_core_web_sm')
            incoming_question = preprocess(normalize_string(nlp(sentence)))
            

            # # print("=======> Before normalizing : ",sentence)
            # s1 = nlp(sentence)
            # s1 = normalize_string(str(s1))
            print("=======> After calling function normalize_string : ", incoming_question)
            # ps = PorterStemmer()
            # s1_stem = ""
            # for word in s1:
            #     rootWord = ps.stem(str(word))
            #     s1_stem += rootWord
            # # nlpString1 = nlp(s1_stem)
            # # print(nlpString1)
            response = jsonify({
                'data': incoming_question
            })
            response.status_code = 200
            return response
    return app
