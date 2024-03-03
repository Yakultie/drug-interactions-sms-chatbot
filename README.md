# Drug Interactions SMS Chatbot

## How do I run the chatbot?
### Clone this repository
Run the following command in the directory you wish to clone this project to:
```
git clone https://github.com/Yakultie/drug-interactions-sms-chatbot
```

### Install dependencies
In the root directory of the project, run the following command to install all the necessary dependencies:
```
pip3 install -r requirements.txt
```

### Set your environment variables
Replace the values with your actual connection strings, URLs, secret keys, and Twilio number. Then, run the following commands in the terminal you plan to use:
```
export MONGODB_CONNECTION_STRING=mongodb+srv://XXXXX:XXXXX@XXXXX/?authMechanism=DEFAULT;
export DRUGBANK_API_URL=https://XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX;
export OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX;
export TWILIO_ACCOUNT_SID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX;
export TWILIO_AUTH_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX;
export CHATBOT_NUMBER=XXXXXXXXXXX;
```

### Run the Flask server for Twilio to call
In the root directory of the project, run the following command to run the Flask server:
```
flask run
```
Then, update your settings for the Twilio number so that the Webhook URL field points to the Flask server.
<br/><br/>
<img src="https://i.imgur.com/KluTuru.png" width="768"/>

### Query the chatbot
Send a text message to the Twilio number you assigned to this project, and wait for the ✨ magic ✨ to happen!
<br/><br/>
<img src="https://i.imgur.com/C5FNQUM.jpg" width="256"/>
