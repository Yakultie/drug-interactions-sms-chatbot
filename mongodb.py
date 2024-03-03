import os
import pymongo
from datetime import datetime

mongo_client = pymongo.MongoClient(os.environ["MONGODB_CONNECTION_STRING"])
mongo_db = mongo_client["medinfo"]
mongo_collection = mongo_db["interactions"]
mongo_statuses = mongo_db["session_statuses"]

def userInSession(userId):
    user_status = mongo_statuses.find_one({"userId": userId})
    if not user_status:
        record = { "userId": userId, "entered_session": None }
        mongo_statuses.insert_one(record)
        return False
    
    entered_session = user_status["entered_session"]
    if not entered_session:
        return False
    
    delta = datetime.now() - entered_session
    if delta.total_seconds() >= 300:
        return False
    
    return True

def recordNewSession(userId):
    user_status = mongo_statuses.find_one({"userId": userId})
    found_id = user_status["_id"]
    user_status["entered_session"] = datetime.now()
    mongo_statuses.delete_one({'_id': found_id})
    mongo_statuses.insert_one(user_status)

def recordEndSession(userId):
    user_status = mongo_statuses.find_one({"userId": userId})
    found_id = user_status["_id"]
    user_status["entered_session"] = None
    mongo_statuses.delete_one({'_id': found_id})
    mongo_statuses.insert_one(user_status)

def retrieveUserSessionTimestamp(userId):
    user_status = mongo_statuses.find_one({"userId": userId})
    return user_status["entered_session"]

def retrieveUserInteractions(userId):
    return mongo_collection.find_one({"userId": userId})

def recordUserInteraction(userId, role, message):
    existing_document = retrieveUserInteractions(userId)

    record = {
                "role": role,
                "message": message,
                "timestamp": datetime.now()
            }
    
    if existing_document:
        found_id = existing_document["_id"]
        existing_document["history"].append(record)
        mongo_collection.delete_one({'_id': found_id})
        mongo_collection.insert_one(existing_document)
    
    else:
        new_document = { "userId": userId, "history": [] }
        new_document["history"].append(record)
        mongo_collection.insert_one(new_document)
    
def retrieveUserMessages(userId):
    existing_document = retrieveUserInteractions(userId)
    messages = []

    for message in existing_document["history"]:
        if message["role"] == "user":
            messages.append(message["message"])
    
    return messages

def retrieveUserMessagesBeforeCurrentSession(userId):
    existing_document = retrieveUserInteractions(userId)
    timestamp = retrieveUserSessionTimestamp(userId)
    
    messages = []

    for message in existing_document["history"]:
        if message["timestamp"] < timestamp and message["role"] == "user":
            messages.append(message["message"])
    
    return messages

def retrieveUserMessagesAfterTimestamp(userId, timestamp):
    existing_document = retrieveUserInteractions(userId)
    messages = []

    for message in existing_document["history"]:
        if message["timestamp"] > timestamp and message["role"] == "user":
            messages.append(message["message"])
    
    return messages
