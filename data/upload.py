import json
import time
import datetime
import pymongo
from pymongo import MongoClient

# Creating variables for time
t = time.localtime()
timestamp = time.strftime('%b-%d-%Y', t)

# Finding the files for upload
# Looks for files named specifically " " + timestamp
# Only uploads the files from the current date
dict_log = "dict_" + timestamp
adc_log = "adc_" + timestamp
rgb_log = "rgb_" + timestamp
acc_log = "acc_" + timestamp
hot_log = "hot_" + timestamp

# Connect to the mongodb client with correct credentials
# //Username::Password @ MongoDB server
client = pymongo.MongoClient("mongodb+srv://Ryan:Fablab1@biofinder-rgsud.gcp.mongodb.net/admin")

# Accessing the MongoDB Client
db = client['BioFinder']

# Finding the collection name to write the data in
dict_data = db['Level']
adc_data = db['ADC']
rgb_data = db['RGB']
acc_data = db['ACC']
hot_data = db['HOT']

print "Uploading data..."

# Opening the files so we can upload them
with open('%s.json' % dict_log) as f:
        # Opening the .json file to read data
        file_data = json.load(f)
        # Inserting the data into the file to upload
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
# Closing the client
client.close()
