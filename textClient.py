from twilio.rest import Client
from config import auth_token, account_sid

client = Client(account_sid, auth_token)


def sendSMS(number, message):
    print(message)
    message = client.messages.create(
        to=number,
        from_="3012152256",
        body=message
    )
    print(message.sid)


def getSMS():
    message = client.messages.get()
