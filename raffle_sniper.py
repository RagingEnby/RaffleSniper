import requests
import time
import base64
from nbt import nbt
from io import BytesIO
from numerize import numerize
import datetime
import json

with open('config', 'r') as file:
  config = json.load(file)


def GET_ITEM_WEBHOOK(itemID):
  if itemID in config['webhooks']: return config['webhooks'][itemID]

  elif 'DYE' in config['webhooks'] and config['webhooks']['DYE'] != 'DYE_WEBHOOK_URL' and itemID.startswith('DYE_'): return config['webhooks']['DYE']

  else: return config['webhooks']['DEFAULT']


def GET_IGN(uuid):
  mojang_response = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
  if mojang_response.status_code == 200:
    if 'name' in mojang_response.json():
      return mojang_response.json()['name']
    else: return uuid
  else: return uuid

first_update = requests.get(config['auctionApi'])
first_update_data = first_update.json()
lastlastUpdated = int(first_update_data['lastUpdated'])

while True:
  data = requests.get(config['auctionApi']).json()
  if data['lastUpdated'] != lastlastUpdated:
    before_refresh_time = time.time()

    for auction in data["auctions"]:
      if auction['start'] < lastlastUpdated: continue
      nbt_data = nbt.NBTFile(fileobj=BytesIO(base64.b64decode(auction['item_bytes'])))
      if 'ExtraAttributes' not in nbt_data['i'][0]['tag']: continue
      extraAttributes = nbt_data['i'][0]['tag']['ExtraAttributes']
      if 'raffle_year' not in extraAttributes: continue

      # By this point, all non-raffle auctions are filtered :)
      item_id = nbt_data['i'][0]['tag']['ExtraAttributes']['id']
      raffle_year = extraAttributes['raffle_year']
      auctioneer_ign = GET_IGN(auction['auctioneer'])
      price_field_name = "Price" if auction['bin'] else "Starting Bid"
      price_field_value = numerize.numerize(auction['starting_bid'])
      raffle_win_split = str(extraAttributes['raffle_win']).split('_')
      raffle_info = f"{raffle_win_split[2].capitalize()} Raffle #{int(raffle_win_split[3]) + 1}"
      raffle_info = raffle_info.replace('Small', 'Speed').replace('Medium', 'Daily').replace('Large #1', 'The Big One')
      if config['extraAttributeDisplay']: description = "```" + "\n".join([f"{key}: {value}" for key, value in nbt_data['i'][0]['tag']['ExtraAttributes'].items()]) + "```"
      else: description = ""
      embed = {
          "content": "",
          "embeds": [
          {
            "title": auction['item_name'],
            "description": description,
            "url": f"https://sky.coflnet.com/auction/{auction['uuid']}",
            "color": 0x00AA00,
            "fields": [
              {
                "name": f"{price_field_name}",
                "value": f"{price_field_value}",
                "inline": True
              },
              {
                "name": "Raffle",
                "value": f"{raffle_info}",
                "inline": True
              }
              ],
                "author": {
                  "name": f"{auctioneer_ign}",
                  "icon_url": f"https://mc-heads.net/head/{auction['auctioneer']}"
                },
              "footer": {
                "text": f"/viewauction {auction['uuid']}"
              },
              "thumbnail": {
              "url": f"https://sky.shiiyu.moe/item/{item_id}"
              }
            }
          ],
          "username": 'Skypixel',
          "avatar_url": 'https://github.com/RagingEnby/SkypixelRepo/blob/main/skypixel.png?raw=true'
      }
      requests.post(GET_ITEM_WEBHOOK(str(item_id)), json=json.dumps(embed), headers={"content-type": "application/json"})

    if 'LOG_WEBHOOK' in config['webhooks'] and config['webhooks']['LOG_WEBHOOK'] != 'LOG_WEBHOOK_URL':
      lastlastUpdated = data['lastUpdated']
      refresh_time = round(time.time() - before_refresh_time, 4)
      embed = {
        "content":
        "",
        "embeds": [{
          "title": "Refresh Completed",
          "color": 16755200,
          "footer": {
            "text": f"{refresh_time * 1000}ms"
          },
          "timestamp": f"{datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'}"
        }],
        "username": 'Skypixel',
        "avatar_url": 'https://github.com/RagingEnby/SkypixelRepo/blob/main/skypixel.png?raw=true',
        "flags": 4096
      }
      response = requests.post(config['webhooks']['LOG_WEBHOOK'], data=json.dumps(embed), headers={"Content-Type": "application/json"})
    
  else:
    time.sleep(config['waitBeforeRetry'])