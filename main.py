import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request


# Load Twilio config from .env
from dotenv import load_dotenv
load_dotenv()

ACCOUNT_SID = os.getenv('ACCOUNTSID')
AUTH_TOKEN = os.getenv('AUTHTOKEN')

# Init Twilio Client and Flask
client = Client(ACCOUNT_SID, AUTH_TOKEN)
app = Flask(__name__)

# Now we set up Flask


@app.route('/')
def hello():
    print('HELLO: Recieved A Request')
    return "Hello, World!"


@app.route('/sms', methods=['POST'])
def reply():
    """
    - Respond to twilio messages
    """
    # Fetch the message
    msg = request.form.get('Body')
    print(f"REPLY: The following body was received: {msg}")

    # Define response
    resp = MessagingResponse()

    # Test message
    if msg.strip().lower() == "@test_msg":
        resp.message("Bot is activated and functioning!")


if __name__ == '__main__':
    app.run(debug=True)  # Change this to False
