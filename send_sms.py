from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC3dca027c377008dfd1b2b7eb3f1e74fa"
# Your Auth Token from twilio.com/console
auth_token  = "e48121a4700409657165a671b2608fa7"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+375292264283", 
    from_="+18313465896",
    body="Hello from Python!")

print(message.sid)
