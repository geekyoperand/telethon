import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl import functions, types
import requests
from urllib.parse import unquote

api_id = 6487373
api_hash = '700f3b0513f9a1a321b28d4eed4a4140'
channel_usernames = ['Offerzone_deals', 'Loot_Offers_Dealss', 'Rishavtechnical', 'freekaamaalindia', 'loottimes', 'bigtricksin', 'zingoy', 'Offerzone_Tricks', 'freekamaal7',
                     'kooltech007', 'gopaisadeals', 'deals_velocity_trending_stealsss', 'Deals_Point', 'CashKaroOfficialLootDeals', "best_loot_deals_sale_free", "thetestingphase", "IrfanTechHelper"]
client = TelegramClient('session_name', api_id, api_hash).start()
oldURLs = []


def unshorten_url(url):
    response = requests.get(url)
    return response.url


def isNotFlipkartQuiz(text):
    return text.lower().find("ladies and gentlemen") == -1 and text.lower().find("kya bolti public") == -1 and text.lower().find("daam sahi hai") == -1 and text.lower().find("fake or not") == -1 and text.lower().find("fake or not fake") == -1 and text.lower().find("khel paheliyon ka") and text.lower().find("daam sahi hai") and text.lower().find("sirf ek minute")


def findAllLinks(text):
    link_regex = re.compile(
        '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    return re.findall(link_regex, text)


def checkAndUpdateLinkRedirectURL(url, file):
    if url.find("linkredirect.in") != -1:
        link_redirect_body = requests.get(url).text
        link_redirect_urls = findAllLinks(link_redirect_body)
        if len(link_redirect_urls) >= 3 and len(link_redirect_urls[2]) >= 1:
            url = link_redirect_urls[2][0]
        else:
            url = ""
        file.write("linkredirect.in conversion => : {}\n".format(url))
    if url.find("traqkar.com") != -1:
        splittedUrls = url.split("ckmrdr=")
        url = splittedUrls[1]
        url = unquote(url)
        file.write("traqkar.com conversion => : {}\n".format(url))

    return url


def removeOriginalSources(text):
    text = text.replace("kooltech.co.in", "")
    text = text.replace("offerzonelootdeals.com", "")
    insensitive_telegram = re.compile(
        re.escape('telegram'), re.IGNORECASE)
    text = insensitive_telegram.sub("", text)
    return text


async def main():
    entity = await client.get_entity("teeeeeeesttttttttnmcfcnm")
    print("Started Listening to the messages")

    @client.on(events.NewMessage(chats=channel_usernames))
    async def main(event):
        text = event.message.text
        links = findAllLinks(text)
        count = len(links)
        file = open("myfile.txt", "a", encoding="utf-8")
        if isNotFlipkartQuiz(text):
            notPosted = 0
            for lnk in links:
                url = unshorten_url(lnk[0])
                file.write(
                    "original lnk[0]: {}\nUnshortened link {}\n".format(lnk[0], url))
                if "youtube.com" in url or "telegram" in url or "telegram" in lnk[0] or "t.me" in lnk[0] or "kooltech.co.in" in lnk[0] or "offerzonelootdeals.com" in lnk[0]:
                    if "https://t.me" in lnk[0] or "telegram" in url or "telegram" in lnk[0]:
                        text = text.replace(
                            lnk[0], "https://t.me/thetestingphase")
                    else:
                        text = text.replace(lnk[0], '')
                        count = count - 1
                    event.message.text = text
                url = checkAndUpdateLinkRedirectURL(url, file)
                file.write("final url: {}\n".format(url))
                if url is not None and len(url) > 0 and url.find("affiliates.sankmo.com") == -1:
                    urlParts = url.split("?")
                    if urlParts[0] in oldURLs:
                        print("---Already Posted----", urlParts[0])
                        file.write("Already Posted: {}\n".format(urlParts[0]))
                    else:
                        oldURLs.append(urlParts[0])
                        notPosted = notPosted + 1
                        if len(oldURLs) == 10000:
                            oldURLs.pop()
                    print(len(oldURLs))
                    file.write("oldURLs: {}\n".format(oldURLs))
            if count > 0 and notPosted > 0:
                event.message.text = removeOriginalSources(text)
                await client.send_message(entity=entity, message=event.message)
                file.write("<== Posted ==>\n")
            else:
                print(text)
                file.write("text => {}\n".format(text))
                file.write("Count: {} and notPosted: {}\n".format(
                    count, notPosted))
                file.write("<== Not Posted ==>\n")
            file.write("--------------------\n\n\n")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
client.run_until_disconnected()
