from flask_api import FlaskAPI
from flask import request, jsonify
from flask_cors import CORS
import pandas as pd
import csv
import re
import numpy as np
from numpy import array
from sklearn import preprocessing
from pprint import pprint
# from tensorflow.keras.models import load_model
# import tensorflow as tf
import spacy
import nltk
from nltk.stem import PorterStemmer
import requests
import json

pd.set_option('display.max_colwidth', -1)


def normalize_string(string):
    test_string = ""
    for word in string:
        test_string += word.text.lower()
        test_string += " "
    synonym_dict = get_dict()

    for key in synonym_dict:
        for t in key:
            strng = t.lower()
            if strng in test_string:
                test_string = test_string.replace(strng, synonym_dict[key])

    return (test_string)


def get_dict():

    compare = ['F1 student','SJSU','San Jose State University','ISSS', 'International student and scholar services',
    'International','Graduate admissions and program evaluation',"graduate", "application", "deadline"
    'GAPE',"MSSE",'MSISE','CMPE','WST','GPA','MSCS',"full time",
    'Masters of Science in Software Engineering','Masters', "Health center","health","appointment",
    'Admission',"Software Engineering","Engineering","Writing skills test","Open University","Grade point average"]
    
    
    
    return compare


def create_app():
    app = FlaskAPI(__name__, instance_relative_config=True)

    CORS(app)

    @app.route('/question/', methods=['POST'])
    def ask():
        if request.method == "POST":
            chatbot_data = pd.read_csv(
                "C:\\Users\\Reeya\\OneDrive\\Desktop\\CMPE295B\\Backend\\app\\chatbot_data.csv")
            # chatbot_data = pd.read_csv('/Users/kavinadesai/Desktop/SJSU/Sem4/CMPE295B-Eirinaki/web-crawler/Servers/Backend/app/chatbot_data.csv')
            incoming_question = str(request.data.get('question'))
            context = str(request.data.get('context'))
            print("========> The Context is : ", context)
            
            incoming_question = incoming_question.lower()
            
            
            synonym_dict = get_dict()
            flag = 0
            for key in synonym_dict:
                key = key.lower()
                if key in incoming_question:
                    print(key)
                    print(incoming_question)
                    flag = 1
                    break

            if(flag == 1):
                url = "http://localhost:5001/nlp-normalize/"
                options = {'question': incoming_question}
                preprocessed = requests.post(url, data=options)
                preprocessed = preprocessed.json()
                print("======> Data returned from nlp-normalize API  : \n", preprocessed)

                url = "http://localhost:5002/similarity/"
                options = {
                    'normalized_incoming': preprocessed['data'], "context": context}
                matchedQuestion = requests.post(url, data=options)
                matchedQuestion = matchedQuestion.json()
                print("======> Data returned from similarity API  : \n",
                      matchedQuestion)
                print("\n\n\n")
                print(" matchedQuestion[data] : ", matchedQuestion["data"])

                response = jsonify({
                    'answer': matchedQuestion["data"],
                    'context': matchedQuestion["context"]
                })
                response.status_code = 200
                return response
            else:
                url = "http://localhost:8080/programab"
                options = {"question": incoming_question}
                answer_from_ab = requests.post(url, data=json.dumps(options))

                answer_from_ab = answer_from_ab.text
                index = answer_from_ab.find("?")
                index = -1
                if(index == -1):
                    response = jsonify({
                        'answer': answer_from_ab
                    })
                    response.status_code = 200
                    return response
                else:
                    url = "http://localhost:5001/nlp-normalize/"
                    options = {'question': incoming_question}
                    preprocessed = requests.post(url, data=options)
                    preprocessed = preprocessed.json()
                    print("======> Data returned from nlp-normalize API  : \n", preprocessed)

                    url = "http://localhost:5002/similarity/"
                    options = {
                        'normalized_incoming': preprocessed['data'], "context": context}
                    matchedQuestion = requests.post(url, data=options)
                    matchedQuestion = matchedQuestion.json()
                    print("======> Data returned from similarity API  : \n",
                        matchedQuestion)
                    print("\n\n\n")
                    print(" matchedQuestion[data] : ", matchedQuestion["data"])

                    response = jsonify({
                        'answer': matchedQuestion["data"],
                        'context': matchedQuestion["context"]
                    })
                    response.status_code = 200
                    return response
   
    return app
