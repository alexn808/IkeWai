import json
import pymongo
from pymongo import MongoClient

#//USERNAME:PASSWORD@HOSTNAME/Database
client = pymongo.MongoClient("mongodb+srv://Ryan:Fablab1@biofinder-rgsud.gcp.mongodb.net/")
db = client['BioFinder']
test_data = db['Test']

with open('test.json') as f:
    file_data = json.load(f)

test_data.insert(file_data)
client.close()

