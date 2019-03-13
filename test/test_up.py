import json
import urllib2
import pymongo
from pymongo import MongoClient


client = pymongo.MongoClient("mongodb+srv://Ryan:Fablab1@biofinder-rgsud.gcp.mongodb.net/admin")
db = client['BioFinder']
test_data = db['Test']

with open('import.json') as f:
	file_data = json.load(f)

	test_data.insert(file_data)
client.close()
