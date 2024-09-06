from Database_conn import COLLECTION_NAME,CONNECTION_STRING,DATABASE_NAME
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def database_connection():

    try:
        client = MongoClient(CONNECTION_STRING)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        return collection
        print("Connected to Cosmos MongoDB!")
        
    except ConnectionFailure as e:
        print(f"Connection failed: {e}")


if __name__ == "__main__":
    print()