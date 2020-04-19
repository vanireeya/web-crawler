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

def create_app():
    app = FlaskAPI(__name__, instance_relative_config=True)

    CORS(app)

    @app.route('/similarity/', methods=['POST'])
    def ask():
        if request.method == "POST":
            nlp_data = pd.read_csv("C:\\Users\\Reeya\\OneDrive\\Desktop\\CMPE295B\\Similarity\\app\\data.csv")
            nlp = spacy.load('en_core_web_sm')
            r, c = nlp_data.shape
            incoming_question = request.data.get('normalized_incoming')
            column_names = ["Questions", "Similarity score","Original"]
            similarity_df = pd.DataFrame(columns = column_names)
            for i in range(0,r):
                database_question = nlp_data.loc[i][1]
                original_question = nlp_data.loc[i][0]
                similarity_score = nlp(incoming_question).similarity(nlp(database_question))
                similarity_df = similarity_df.append(pd.Series([database_question, similarity_score,original_question], index=similarity_df.columns ), ignore_index=True)
            similarity_df = similarity_df.sort_values(by ='Similarity score', ascending=False )
            
            response = jsonify({
                'data': similarity_df.loc[0][2]
            })
            response.status_code = 200
            return response
    return app



