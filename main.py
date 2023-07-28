import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
from dbManager import DBManager
from revChatGPT.V1 import Chatbot


# Load Twilio config from .env
from dotenv import load_dotenv
load_dotenv()

ACCOUNT_SID = os.getenv('ACCOUNTSID')
AUTH_TOKEN = os.getenv('AUTHTOKEN')

# Init Twilio Client and Flask
client = Client(ACCOUNT_SID, AUTH_TOKEN)
app = Flask(__name__)

# Get an instance of DbManager
dbManager = DBManager()

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

    # Test message
    if msg.strip().lower() == "@test_msg":
        message = client.messages.create(
            body='Hello there! Bot is up and running!',
            from_='whatsapp:+14155238886',
            to=fromnum
        )
        return
    elif msg.strip().lower() == '!start':
        # All we need is a new conversation ID to restart the conversation
        dbManager.remove_conversation_id(fromnum)
        dbManager.create_new_row(fromnum)

        message = client.messages.create(
            body='Alright! A New Conversation has been started for you!',
            from_='whatsapp:+14155238886',
            to=fromnum
        )
        return

    elif msg.strip().lower() == '!help':
        message = client.messages.create(
            body="Don't Fret! I'm here to help! I am a Whatsapp bot that uses ChatGPT! To restart a conversation, simply type: '!start'. And that's about it!",
            from_='whatsapp:+14155238886',
            to=fromnum
        )
        return

    # Now we can use RevChatGPT to create a conversation
    chatbot = Chatbot(config={
        "email": "example@example.com",
        "password": "password1234"
    })

    response = ""
    for data in chatbot.ask(prompt):
        response = data["message"]

    message = client.messages.create(
        body=response,
        from_='whatsapp:+14155238886',
        to=fromnum
    )


if __name__ == '__main__':
    app.run(debug=True)
