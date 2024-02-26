from pymongo import MongoClient
import os
import logging
def connect_to_mongo() -> MongoClient:
    host = os.environ.get('MONGO_HOST')
    port = int(os.environ.get('MONGO_PORT', '27017'))
    user = os.environ.get('MONGO_USER')
    password = os.environ.get('MONGO_PASS')
    client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}/admin')
    print('Connected to MongoDB!')
    return client