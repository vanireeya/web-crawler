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

pd.set_option('display.max_colwidth', -1)

def create_app():
    app = FlaskAPI(__name__, instance_relative_config=True)

    CORS(app)

    @app.route('/question/', methods=['POST'])
    def ask():
        if request.method == "POST":
            # chatbot_data = pd.read_csv("C:\\Users\\Reeya\\OneDrive\\Desktop\\CMPE295B\\Backend\\app\\chatbot_data.csv")
            chatbot_data = pd.read_csv('/Users/kavinadesai/Desktop/SJSU/Sem4/CMPE295B-Eirinaki/web-crawler/Servers/Backend/app/chatbot_data.csv')
            incoming_question = str(request.data.get('question'))
            print("========> The incoming question is : ", incoming_question)
            url = "http://localhost:5001/nlp-normalize/"
            options = {'question': incoming_question}
            preprocessed = requests.post(url, data=options)
            preprocessed = preprocessed.json()
            print("======> Data returned from nlp-normalize API  : \n", preprocessed)
            url = "http://localhost:5002/similarity/"
            options = {'normalized_incoming': preprocessed['data']}
            matchedQuestion = requests.post(url, data=options)
            matchedQuestion = matchedQuestion.json()
            print("======> Data returned from similarity API  : \n", matchedQuestion)
            print(" matchedQuestion[data] : ", matchedQuestion["data"])
            found = chatbot_data[chatbot_data['Question'].str.contains(matchedQuestion["data"], na=False)]
            print("FOUND!!!!!\n", found)
            ans = found['Answer'].to_string()
            ans = ans[3:]
            ans = re.sub(' +', ' ', ans).strip()
            print("Final answer : \n",ans)

            # filter1 = chatbot_data["Question"] == matchedQuestion["data"]
            # print("filter : ", filter1)
            # chatbot_data.where(filter1, inplace = True) 
            response = jsonify({
                'answer': ans
            })
            response.status_code = 200
            return response
    return app

