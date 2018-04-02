#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import requests
import json
import re

app = Flask(__name__)
ACCESS_TOKEN = ''
VERIFY_TOKEN = ''
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
                lmessage = message['message'].get('text').lower()
                recipient_id = message['sender']['id']
                # if message['message'].get('text'):
                    # response_sent_text = get_message()
                    # send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
                if "all" in message['message'].get('text').lower():
                    response_sent_nontext = getallflatmates()
                    send_message(recipient_id, response_sent_nontext)
                if "home" in message['message'].get('text').lower():
                    response_sent_nontext = gethomeflatmates()
                    send_message(recipient_id, response_sent_nontext)
                if "away" in message['message'].get('text').lower():
                    response_sent_nontext = getawayflatmates()
                    send_message(recipient_id, response_sent_nontext)
                if "who is the best" in message['message'].get('text').lower():
                    response_sent_nontext = "Riley is"
                    send_message(recipient_id, response_sent_nontext)
                if "ping" in message['message'].get('text').lower():
                    response_sent_nontext = "pong"
                    send_message(recipient_id, response_sent_nontext)
                if "get lights" in message['message'].get('text').lower():
                    response_sent_nontext = getlights()
                    send_message(recipient_id, response_sent_nontext)
                if "get light " in message['message'].get('text').lower():
                    split = message['message'].get('text').split("get light ")
                    response_sent_nontext = getalight(split[1])
                    send_message(recipient_id, response_sent_nontext)
                if "turn off " in message['message'].get('text').lower():
                    split = lmessage.split("turn off ")
                    changelight(split[1], "off",0, recipient_id)
                if "turn on " in message['message'].get('text').lower():
                    split = lmessage.split("turn on ")   
                    changelight(split[1], "on",100, recipient_id)
                if "dim " in message['message'].get('text').lower():# and " by " in message['message'].get('text').lower():
                    split = lmessage.split("dim ")
                    digits = re.findall(r'\d+', lmessage)
                    item = re.findall(r'(?<=dim )(.*?)(?= by)',lmessage)
                    if not item:
                      item = re.findall(r'(?<=dim )(.*?)(?= to)',lmessage)
                    print (digits[0] + " " + split[1])
                    changelight(item[0], "on",digits[0], recipient_id)
                   
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

def changelight(lightname, state,brightness,recipient_id):
    if getalight(lightname) == "":
      send_message(recipient_id, "light does not exist" )
      send_message(recipient_id, "to list all lights run the following:" )
      send_message(recipient_id, "get lights")
      return 0
    print(len(getalight(lightname)))
    url = 'http://ellerton.nz:8123/api/services/light/turn_' + state
    if "on" in state: 
      payload = {"entity_id": "light." + lightname,"brightness_pct":brightness}
    else:
      payload = {"entity_id": "light." + lightname}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    send_message(recipient_id, lightname + " turned " + state)
 
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
def getalight(lightname):
    data = getdata()
    lights = ""
    for rows in data:
      light = ''
      if "light." in rows['entity_id']:
        if lightname in (rows['attributes']['friendly_name'].lower()):
          entity = rows['entity_id'].split("light.")
          light = ("command: " + entity[1] + "\n" + rows['attributes']['friendly_name'] + ":".ljust(20 - len(rows['attributes']['friendly_name'])) + (rows['state']) + '\n')
          print(light)
        lights += light
    return lights
def getlights():
    data = getdata()
    lights = ""

    #print(getdata())
    for rows in data:
      light = ''
      if "light." in rows['entity_id']:
        #if "router" in rows['attributes']['source_type']:
        #if (rows['attributes']).get('fbt'):
          #if "not_home" not in (rows['state']):
 #         else: status = "Home"
            light = (rows['entity_id'] + " : " + rows['attributes']['friendly_name'] + ":".ljust(20 - len(rows['attributes']['friendly_name'])) + (rows['state']) + '\n')
      lights += light + ""
    return lights
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
    app.run(host='127.0.0.1',port=5000)
