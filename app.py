#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import requests
import json

app = Flask(__name__)
ACCESS_TOKEN = 'EAACxWzzaadcBAAZAUtlmNQHEwGTWrxuSEaivY008Jjl4VRCljPsxLh1raobtS7LfBH9YGWDtTHQXoq2ksx5PssqOZAu3WYGHXd9TrZCospxXn6mhpbFV7ZBGkWzlq07zIdZC0dRidrGvPIlSwjuzQlRXMC5XGeRI9LwLr9uIPdgZDZD'
VERIFY_TOKEN = 'helloworldiam'
bot = Bot(ACCESS_TOKEN)
 
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                # if message['message'].get('text'):
                    # response_sent_text = get_message()
                    # send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
                if "all" in message['message'].get('text'):
                    response_sent_nontext = getallflatmates()
                    send_message(recipient_id, response_sent_nontext)
                if "home" in message['message'].get('text'):
                    response_sent_nontext = gethomeflatmates()
                    send_message(recipient_id, response_sent_nontext)
                if "away" in message['message'].get('text'):
                    response_sent_nontext = getawayflatmates()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"
 
 
def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'
 
 
#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)
 
#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

def getdata():
    req  = requests.get("http://192.168.1.15:8123/api/states")
    data = req.json()
    return data

# def gethomeflatmates():
    # data = getdata()
    # flatmates = ""

   # print(getdata())
    # for rows in data:
      # flatmate = ''
      # if "device_tracker" in rows['entity_id']:
       # if "router" in rows['attributes']['source_type']:
        # if (rows['attributes']).get('fbt'):
          # if "not_home" not in (rows['state']):
            # flatmate = (rows['attributes']['friendly_name'] + " is Home" + '\n')
        # flatmates += flatmate + " "
    # return flatmates

def gethomeflatmates():
    data = getdata()
    flatmates = ""

    #print(getdata())
    for rows in data:
      flatmate = ''
      if "device_tracker" in rows['entity_id']:
        #if "router" in rows['attributes']['source_type']:
        if (rows['attributes']).get('fbt'):
          if "not_home" not in (rows['state']):
 #         else: status = "Home"
            flatmate = (rows['attributes']['friendly_name'] + " is home" + '\n')
      flatmates += flatmate + ""
    return flatmates

def getawayflatmates():
    data = getdata()
    flatmates = ""

    #print(getdata())
    for rows in data:
      flatmate = ''
      if "device_tracker" in rows['entity_id']:
        #if "router" in rows['attributes']['source_type']:
        if (rows['attributes']).get('fbt'):
          if "not_home" in (rows['state']):
 #         else: status = "Home"
            flatmate = (rows['attributes']['friendly_name'] + " is away" + '\n')
      flatmates += flatmate + ""
    return flatmates

def getallflatmates():
    data = getdata()
    flatmates = ""

    #print(getdata())
    for rows in data:
      flatmate = ''
      if "device_tracker" in rows['entity_id']:
        #if "router" in rows['attributes']['source_type']:
        if (rows['attributes']).get('fbt'):
          if "not_home" in (rows['state']): status = "Away"
          else: status = "Home"
          flatmate = (rows['attributes']['friendly_name'] + " is " + status + '\n')
      flatmates += flatmate
    return flatmates

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8098)
