from twilio.rest import Client
from config import auth_token,account_sid

client = Client(account_sid,auth_token)
def sendSMS(number,message):
    print(message)
    message = client.messages.create(
        to=number,
        from_="Twilio Accounts Phone Number Goes Here",
        body=message
    )
    print(message.sid)
