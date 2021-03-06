import json
import datetime
from hikvisionapi import Client
from telethon import TelegramClient, events, sync

with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)
print()

hik_url = data['hik_url']
hik_usr = data['hik_usr']
hik_pwd = data['hik_pwd']

api_id = data['api_id']
api_hash = data['api_hash']
phone = data['phone']

destinations = data['destinations']

client = TelegramClient(phone, api_id, api_hash)
client.start()

if not client.is_user_authorized():
  client.send_code_request(phone)
  client.sign_in(phone, input('Enter the code: '))

def cam_image(channel):
  camshot = cam.Streaming.channels[channel].picture(method='get', type='opaque_data')
  return camshot

def telegram_send(destination, message):
  print('Message send to:' + destination)
  entity=client.get_entity(destination)
  client.send_message(entity, message, parse_mode='html')
  response = cam_image(402)
  client.send_file(entity, response.content, caption="CAM-4")
  
def telegram_multi_send(destinations, message):
  for i in range(len(destinations)):
    telegram_send(destinations[i], message)

cam = Client(hik_url, hik_usr, hik_pwd, timeout=30)

print('TeleHik Started . . . on ' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

while True:
  try:
    response = cam.Event.notification.alertStream(method='get', type='stream')
    response2 = cam.System.deviceInfo(method='get')
    eventtype = response[0]['EventNotificationAlert']['eventType']
    datetime = response[0]['EventNotificationAlert']['dateTime']
    eventdesc = response[0]['EventNotificationAlert']['eventDescription']
    if response and eventtype == "IO":
      ioport = response[0]['EventNotificationAlert']['inputIOPortID']
      message = "Event Type: " + eventtype + " triggered on " + datetime + " on port: " + ioport
      print(message)
      telegram_multi_send(destinations, message)
           
    elif response and eventtype == "videoloss":
      channelid = response[0]['EventNotificationAlert']['channelID']
      if channelid != "0":
        print(response[0]['EventNotificationAlert']['dateTime'])
        print(response[0]['EventNotificationAlert']['eventType'])
        print(response[0]['EventNotificationAlert']['eventDescription'])
        print(channelid)

  except Exception:
      pass

client.disconnect()


































































































