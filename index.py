import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl import functions, types
import http
import urlexpander
import urllib
import requests

api_id = 6487373
api_hash = '700f3b0513f9a1a321b28d4eed4a4140'
channel_usernames = ['Offerzone_deals', 'Loot_Offers_Dealss', 'Rishavtechnical', 'freekaamaalindia',
                     'loottimes', 'bigtricksin', 'zingoy', 'Offerzone_Tricks', 'freekamaal7', 'kooltech007', 'gopaisadeals', 'deals_velocity_trending_stealsss', 'Deals_Point', 'CashKaroOfficialLootDeals']
client = TelegramClient('session_name', api_id, api_hash).start()


def unshorten_url(url):
    session = requests.Session()
    resp = session.head(url, allow_redirects=True)
    return resp.url


async def main():
    # messages = [];
    entity = await client.get_entity("thetestingphase");
    # print("--1----")
    @client.on(events.NewMessage(chats=channel_usernames))
    async def main(event):
        link_regex = re.compile(
            '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        message = event.message
        text = event.message.text
        links = re.findall(link_regex, text)
        # for lnk in links:
            # url = unshorten_url(lnk[0])
            # print(url)
            # text = text.replace(lnk[0], url)
            # event.message.text = text
        count = len(links)
        for lnk in links:
            if "https://t.me" in lnk[0] or "kooltech.co.in" in lnk[0] or "offerzonelootdeals.com" in lnk[0]:
                if "https://t.me" in lnk[0]:
                    text = text.replace(lnk[0], "https://t.me/thetestingphase")
                else:
                    print(lnk[0])
                    text = text.replace(lnk[0], '')
                event.message.text = text
                count = count - 1;
        if count > 0:
            # print(event.message.text)
            text = text.replace("kooltech.co.in", "")
            text = text.replace("offerzonelootdeals.com", "")
            event.message.text = text
            await client.send_message(entity=entity, message=event.message)
    # @client.on(events.NewMessage(chats=['sankmo_bot']))
    # async def main1(event):
    #     print("------hello----")
    #     messages.append(event.message)
    #     if len(messages) >= 2:
    #         await client.send_message(entity=entity, message=messages[1])
    #         messages.pop();
    #         messages.pop();
    

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
client.run_until_disconnected()
