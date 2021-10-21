import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl import functions, types
import http
import urlexpander
import urllib
import requests
# import numpy as np

api_id = 6487373
api_hash = '700f3b0513f9a1a321b28d4eed4a4140'
channel_usernames = ['Offerzone_deals', 'Loot_Offers_Dealss', 'Rishavtechnical', 'freekaamaalindia',
                    'loottimes', 'bigtricksin', 'zingoy', 'Offerzone_Tricks', 'freekamaal7', 'kooltech007', 'gopaisadeals', 'deals_velocity_trending_stealsss', 'Deals_Point', 'CashKaroOfficialLootDeals',"thetestingphase"]
client = TelegramClient('session_name', api_id, api_hash).start()
oldURLs = [];

def unshorten_url(url):
    session = requests.Session()
    resp = session.head(url, allow_redirects=True)
    return resp.url


async def main():
    entity = await client.get_entity("teeeeeeesttttttttnmcfcnm");
    print("Started Listening to the messages")
    @client.on(events.NewMessage(chats=channel_usernames))
    async def main(event):
        link_regex = re.compile(
            '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        message = event.message
        text = event.message.text
        links = re.findall(link_regex, text)
        count = len(links)
        if text.lower().find("fake or not fake") == -1 and text.lower().find("khel paheliyon ka") and text.lower().find("daam sahi hai") and text.lower().find("sirf ek minute"): 
            notPosted = 0;
            for lnk in links:
                url = unshorten_url(lnk[0])
                if "youtube.com" in url or  "telegram" in url or  "telegram" in lnk[0] or "t.me" in lnk[0] or "kooltech.co.in" in lnk[0] or "offerzonelootdeals.com" in lnk[0]:
                    if "https://t.me" in lnk[0]:
                        text = text.replace(lnk[0], "https://t.me/thetestingphase")
                    else:
                        text = text.replace(lnk[0], '')
                    event.message.text = text
                    count = count - 1;
                if url.find("affiliates.sankmo.com") == -1:
                    urlParts = url.split("?");
                    if urlParts[0] in oldURLs:
                        print("---Already Posted----",urlParts[0]);        
                    else:
                        oldURLs.append(urlParts[0]);
                        notPosted = notPosted + 1;
                        if len(oldURLs) == 10000:
                            oldURLs.pop();
                    print(len(oldURLs))

            if count > 0 and notPosted > 0:
                text = text.replace("kooltech.co.in", "")
                text = text.replace("offerzonelootdeals.com", "")
                insensitive_telegram = re.compile(re.escape('telegram'), re.IGNORECASE)
                text = insensitive_telegram.sub("", text)
                event.message.text = text
                await client.send_message(entity=entity, message=event.message)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
client.run_until_disconnected()
