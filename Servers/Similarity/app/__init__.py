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
import json

nlp = spacy.load('en_core_web_sm')

# def find_similarity(ques1, ques2):
#     ques1 = nlp(str(ques1))
#     ques2 = nlp(str(ques2))

#     ps = PorterStemmer()
    
#     s1_stem = ""
#     s2_stem = ""
    
#     for word in ques1:
#         rootWord = ps.stem(str(word))
#         s1_stem += rootWord
    
#     for word in ques2:
#         rootWord = ps.stem(str(word))
#         s2_stem += rootWord

#     similarity_score = nlp(s1_stem).similarity(nlp(s2_stem))
    
#     return similarity_score
def find_similarity(sentence_1, sentence_2):
    
    similarity_score = nlp(sentence_1).similarity(nlp(sentence_2))
    return similarity_score


def get_categories():
    categories = ['msise',
                  'f1 student',
                  'admissions',
                  'gape',
                  'misc',
                  'msse',
                  'cmpe',
                  'wst',
                  'major',
                  'ou',
                  'graduation',
                  'financial aid',
                  'mscs',
                  'isss',
                  'library',
                  'health center',
                  'sports',
                  'canvas',
                  'zoom']
    return categories


def create_app():
    app = FlaskAPI(__name__, instance_relative_config=True)

    CORS(app)

    @app.route('/similarity/', methods=['POST'])
    def ask():
        if request.method == "POST":
            chatbot_data = pd.read_csv("C:\\Users\\Reeya\\OneDrive\\Desktop\\CMPE295B_repo\\web-crawler\\Servers\\Similarity\\app\\chatbot_data.csv")
            nlp_data = pd.read_csv("C:\\Users\\Reeya\\OneDrive\\Desktop\\CMPE295B_repo\\web-crawler\\Servers\\Similarity\\app\\data.csv")
            Bot_data_df = pd.read_csv("C:\\Users\\Reeya\\OneDrive\\Desktop\\CMPE295B_repo\\web-crawler\\Servers\\Similarity\\app\\Bot_data.csv")
            incoming_question = request.data.get('normalized_incoming')
            
            
            context = request.data.get('context')
            Bot_data_df.drop(Bot_data_df.columns[0], axis=1,inplace=True)
            print("context: ",context,"\n")

            Bot_data = Bot_data_df.astype(str).values.tolist()
            # print("\n",Bot_data,"\n")

            # print(len(Bot_data))
            # print(len(chatbot_data))
            flag = 0
            prev_word = ""
            # context = ""
            Categories = get_categories()
            nlp = spacy.load('en_core_web_sm')
            for word in nlp(incoming_question):
                if word.text.lower() in Categories:
                    context = word.text
                    flag = 1
                    break
                elif (prev_word + " " + word.text.lower()) in Categories:
                    context = prev_word + " " + word.text.lower()
                    flag = 1
                    break
                else:
                    prev_word = word.text.lower()

            if flag == 0:
                incoming_question += context

            # convert Bot_data to list---------------------------
            m = 0.0
            index = 0
            for i in range(0,len(Bot_data)):
                if (chatbot_data.loc[i][3].lower() != context.lower()):
                    continue;
                # print(Bot_data[i]) 
                # print(chatbot_data.loc[i][3].lower())   
                sim = find_similarity(incoming_question, Bot_data[i][0] + chatbot_data.loc[i][3].lower())
                if (sim > m):
                    m = sim
                    index = i;


            print(chatbot_data.loc[index][1])
            # response = json.dumps({
            #     'data': chatbot_data.loc[index][1], 'context' :context

            # })

            response = jsonify({
                'data': chatbot_data.loc[index][1], 'context' :context

            })
            response.status_code = 200
            return response











            # # nlp_data = pd.read_csv('/Users/kavinadesai/Desktop/SJSU/Sem4/CMPE295B-Eirinaki/web-crawler/Servers/Similarity/app/normalized_chatabot_dataset_new.csv')
            # nlp = spacy.load('en_core_web_sm')
            # r, c = nlp_data.shape
            # print("+ + + + + + + + + + + + + + + + + + + + Data read is : ", nlp_data.head(10))
            # normalized_incoming_question = request.data.get('normalized_incoming')
            # # column_names = ["Questions", "Similarity score", "Original"]
            # # similarity_df = pd.DataFrame(columns = column_names)

            # column_names = ["Original question", "Normalized Questions", "Similarity score"]
            # similarity_df = pd.DataFrame(columns = column_names)

            # for i in range(0,r):
            #     database_question = nlp_data.loc[i][1]
            #     original_database_question = nlp_data.loc[i][0]
            #     # similarity_score = nlp(incoming_question).similarity(nlp(database_question))
            #     similarity_score = nlp(str(normalized_incoming_question)).similarity(nlp(str(database_question)))
            #     # similarity_df = similarity_df.append(pd.Series([database_question, similarity_score,original_question], index=similarity_df.columns ), ignore_index=True)
            #     similarity_df = similarity_df.append(pd.Series([original_database_question, database_question, similarity_score], index=similarity_df.columns ), ignore_index=True)
            #     similarity_df = similarity_df.sort_values(by ='Similarity score', ascending=False )

            # print("__________________ Similarity df : _________________\n", similarity_df.head(10))
            # response = jsonify({
            #     'data': similarity_df.loc[0][0]
            # })
            # response.status_code = 200
            # return response
    return app



