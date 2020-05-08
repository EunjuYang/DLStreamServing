from pymongo import MongoClient
import os
import numpy as np
import random
import time

ip = os.environ['MONGO_PORT_27017_TCP_ADDR']
port = os.environ['MONGO_PORT_27017_TCP_PORT']

client = MongoClient(ip, int(port))
db = client['inference'] # inference database
collection = db[os.environ['NAME']] # model name
post = {}

while True:
    # The number of AMI ID is 5
    for i in range(5):
        batch_size = random.randint(1,10) # batch size is variant.
        post['amiid'] = i
        post['pred'] = np.random.random(batch_size).tolist() # shape is (batch,)
        post['true'] = np.random.random(batch_size).tolist() # shape is (batch,)
        post['timestamp'] = time.time()
        collection.insert_one(post)
    time.sleep(5) # waiting 5 seconds