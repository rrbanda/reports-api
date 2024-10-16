# app/database.py

import os
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "patient_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "patients")

def get_mongo_client(uri, retries=5, delay=3):
    for attempt in range(retries):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # The ismaster command is cheap and does not require auth.
            client.admin.command('ismaster')
            print("Connected to MongoDB")
            return client
        except ConnectionFailure:
            print(f"Connection to MongoDB failed. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("Could not connect to MongoDB")

client = get_mongo_client(MONGODB_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Create a unique index on study_id to prevent duplicates
collection.create_index("study_id", unique=True)
