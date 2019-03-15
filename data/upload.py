import json
import time
import datetime
import pymongo
from pymongo import MongoClient


t = time.localtime()
timestamp = time.strftime('%b-%d-%Y', t)
dict_log = "dict_" + timestamp
adc_log = "adc_" + timestamp
rgb_log = "rgb_" + timestamp
acc_log = "acc_" + timestamp
hot_log = "hot_" + timestamp

client = pymongo.MongoClient("mongodb+srv://Ryan:Fablab1@biofinder-rgsud.gcp.mongodb.net/admin")

db = client['BioFinder']
dict_data = db['Test']
adc_data = db['ADC']
rgb_data = db['RGB']
acc_data = db['ACC']
hot_data = db['HOT']
print "Uploading data..."

with open('%s.json' % dict_log) as f:
        file_data = json.load(f)
        dict_data.insert(file_data)

with open('%s.json' % adc_log) as f:
        file_data = json.load(f)
        adc_data.insert(file_data)

with open('%s.json' % rgb_log) as f:
        file_data = json.load(f)
        rgb_data.insert(file_data)

with open('%s.json' % acc_log) as f:
        file_data = json.load(f)
        acc_data.insert(file_data)

with open('%s.json' % hot_log) as f:
        file_data = json.load(f)
        hot_data.insert(file_data)
print "Finished"
client.close()
