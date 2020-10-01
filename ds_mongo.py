import pymongo
from pymongo import MongoClient
from io import open
import os
import json
import ast

cluster = MongoClient("mongodb+srv://db_admin_user:PlatziMaster123@castordams.nocgb.mongodb.net/lets_rommie?retryWrites=true&w=majority")

db = cluster["lets_rommie"]
collection = db["places"]

results = collection.find({"tv":"false"})

#for result in results:
#    print(result)


"""archivos = os.listdir('25-09-2020')

lista_lugares = []




for archivo in archivos:
    contenido_lugar = open('25-09-2020/' + archivo, "r", encoding='utf-8')
    lista_lugares.append(contenido_lugar.read())
    #print(contenido_lugar.read().encode('utf-8'))


for lugar in lista_lugares:
    print(lugar)
    lugar_dict = ast.literal_eval(lugar)
    collection.insert_one(lugar_dict)
"""
