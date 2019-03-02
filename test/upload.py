import json
import urllib2
import pymongo
from pymongo import MongoClient

connection = pymongo.MongoClient("mongodb://localhost")
db=connection.book
record1 = db.book_collection1

record1.drop()

t = time.localtime()
timestamp = time.strftime('%b-%d-%Y_%H%M', t)

parsed = json.loads("dict" + timestamp)

for item in parsed["Records"]:
    record1.insert(item)

#P2

    
client = MongoClient('localhost', 27017)
db = client['countries_db']
collection_currency = db['currency']

with open('currencies.json') as f:
    file_data = json.load(f)

collection_currency.insert(file_data)
client.close()