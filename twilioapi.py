from datetime import datetime
import time
import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
chatbot_number = os.environ['CHATBOT_NUMBER']
client = Client(account_sid, auth_token)

import pymongo
import mongodb

mongo_client = pymongo.MongoClient(os.environ["MONGODB_CONNECTION_STRING"])
mongo_db = mongo_client["medinfo"]
mongo_collection = mongo_db["interactions"]

def getClarification(userId, question):
    message = client.messages \
        .create(
            body = question,
            from_ = chatbot_number,
            to = userId
        )
    
    timestamp = datetime.now()

    messages = mongodb.retrieveUserMessagesAfterTimestamp(userId, timestamp)

    while len(messages) < 1:
        time.sleep(3)
        messages = mongodb.retrieveUserMessagesAfterTimestamp(userId, timestamp)

    print(messages)
    return messages[0]

def deliverFinalAnswer(userId, answer):
    try:
        message = client.messages \
            .create(
                body = answer,
                from_ = chatbot_number,
                to = userId
            )
        
        mongodb.recordUserInteraction(userId, "agent", answer)
        mongodb.recordEndSession(userId)
        return True
    except:
        return False
