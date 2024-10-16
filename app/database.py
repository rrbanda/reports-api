# app/database.py

import os
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://mongodb:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "patient_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "patients")

def get_mongo_client(uri, retries=5, delay=3):
    """
    Attempts to create a MongoClient with retries.

    :param uri: MongoDB URI
    :param retries: Number of retry attempts
    :param delay: Delay between retries in seconds
    :return: MongoClient instance
    :raises Exception: If connection fails after retries
    """
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

# Initialize MongoDB client
client = get_mongo_client(MONGODB_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Create a unique index on study_id to prevent duplicates
collection.create_index("study_id", unique=True)
