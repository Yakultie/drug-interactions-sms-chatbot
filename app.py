from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import agent
import mongodb

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    question = request.values.get('Body', None)
    sender = request.values.get('From', None)

    if not mongodb.userInSession(sender):
        mongodb.recordNewSession(sender)
        mongodb.recordUserInteraction(sender, "user", question)
        agent.entry_point(sender, question)
    else:
        mongodb.recordUserInteraction(sender, "user", question)
    
    return

if __name__ == "__main__":
    app.run(debug=True, port=5002)
