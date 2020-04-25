from flask_api import FlaskAPI
from flask import request, jsonify
from flask_cors import CORS
import pandas as pd
import csv
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

nlp = spacy.load('en_core_web_sm')

def find_similarity(ques1, ques2):
    ques1 = nlp(str(ques1))
    ques2 = nlp(str(ques2))

    ps = PorterStemmer()
    
    s1_stem = ""
    s2_stem = ""
    
    for word in ques1:
        rootWord = ps.stem(str(word))
        s1_stem += rootWord
    
    for word in ques2:
        rootWord = ps.stem(str(word))
        s2_stem += rootWord

    similarity_score = nlp(s1_stem).similarity(nlp(s2_stem))
    
    return similarity_score


def create_app():
    app = FlaskAPI(__name__, instance_relative_config=True)

    CORS(app)

    @app.route('/similarity/', methods=['POST'])
    def ask():
        if request.method == "POST":
            # nlp_data = pd.read_csv("C:\\Users\\Reeya\\OneDrive\\Desktop\\CMPE295B\\Similarity\\app\\data.csv")
            nlp_data = pd.read_csv('/Users/kavinadesai/Desktop/SJSU/Sem4/CMPE295B-Eirinaki/web-crawler/Servers/Similarity/app/normalized_chatabot_dataset_new.csv')
            nlp = spacy.load('en_core_web_sm')
            r, c = nlp_data.shape
            print("+ + + + + + + + + + + + + + + + + + + + Data read is : ", nlp_data.head(10))
            normalized_incoming_question = request.data.get('normalized_incoming')
            # column_names = ["Questions", "Similarity score", "Original"]
            # similarity_df = pd.DataFrame(columns = column_names)

            column_names = ["Original question", "Normalized Questions", "Similarity score"]
            similarity_df = pd.DataFrame(columns = column_names)

            for i in range(0,r):
                database_question = nlp_data.loc[i][1]
                original_database_question = nlp_data.loc[i][0]
                # similarity_score = nlp(incoming_question).similarity(nlp(database_question))
                similarity_score = nlp(str(normalized_incoming_question)).similarity(nlp(str(database_question)))
                # similarity_df = similarity_df.append(pd.Series([database_question, similarity_score,original_question], index=similarity_df.columns ), ignore_index=True)
                similarity_df = similarity_df.append(pd.Series([original_database_question, database_question, similarity_score], index=similarity_df.columns ), ignore_index=True)
                similarity_df = similarity_df.sort_values(by ='Similarity score', ascending=False )

            print("__________________ Similarity df : _________________\n", similarity_df.head(10))
            response = jsonify({
                'data': similarity_df.loc[0][0]
            })
            response.status_code = 200
            return response
    return app



