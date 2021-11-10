import json
import datetime
from hikvisionapi import Client
from telethon import TelegramClient, events, sync

hik_url = 'http://192.168.10.1'
hik_usr = 'admin'
hik_pwd = 'password'

api_id = 10404010
api_hash = ''
phone = '+27803008020'

destinations = ['me','+27070290000']

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
  with open('screen.jpg', 'wb') as f:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
  client.send_file(entity, r"C:\Users\alber\python\screen.jpg", caption="It's me!")
  

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


































































































