import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl import functions, types
import requests
from urllib.parse import unquote
import json

api_id = 6487373
api_hash = '700f3b0513f9a1a321b28d4eed4a4140'
channel_usernames = ["kooltech007", "Offerzone_deals", "Loot_Offers_Dealss", "Rishavtechnical", "freekaamaalindia", "loottimes", "bigtricksin", "zingoy", "Offerzone_Tricks", "thetestingphase",
                     "freekamaal7", "gopaisadeals", "deals_velocity_trending_stealsss", "Deals_Point", "CashKaroOfficialLootDeals", "Best_Loot_Deals_Sale_Free_Offers", "IrfanTechHelper", "CKoffers", "rapid_loot_deal"]
client = TelegramClient("session_name", api_id, api_hash).start()
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


def changeLinkID(unshortenedUrl, textUrl, text):
    updatedUrl = unshortenedUrl
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '454',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '_xsrf=5f7720bfcf79491fbe48d06c6ee45f5e; anon_u=cHN1X19lNDhjNTdjNi1hYzIxLTQ2MzAtYmFmZi05MTkzNjVkODQ0MWE=|1634892423|ee2d4502a4ec8d09e2766a372630b99b96ee8b2f; optimizelyEndUserId=oeu1634892421291r0.43377463188643617; _gcl_au=1.1.1069873274.1634892422; _mkto_trk=id:754-KBJ-733&token:_mch-bitly.com-1634892422140-61949; _ga=GA1.2.1729876833.1634892422; _gid=GA1.2.1321869772.1634892422; wow-modal-id-10=yes; anon_shortlinks=https://go.aws/3GdnfQD,https://amzn.to/2ZeoEp2; cookie_banner=1; _ga_567GCTL9BB=GS1.1.1634892421.1.1.1634892494.60',
        'origin': 'https://bitly.com',
        'referer': 'https://bitly.com/',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrftoken': '5f7720bfcf79491fbe48d06c6ee45f5e'
    }
    payload = {
        'url': unshortenedUrl
    }

    data = requests.post("https://bitly.com/data/anon_shorten",
                         headers=headers, data=payload)
    if data.status_code == 200:
        print("-----unshortenedUrl-----", unshortenedUrl)
        print("-----textUrl-----", textUrl)
        updatedUrl = json.loads(data.text)['data']['link']
        text = text.replace(textUrl, updatedUrl)
        print("-----updatedUrl-----", updatedUrl)
    return text


def checkAndGenerate3rdPartyAffiliateLink(url, urlWithoutAffId, file):
    isEkaroAffiliationURLCreated = 0
    datalink = url
    if "flipkart.com" in url:
        datalink = urlWithoutAffId
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'content-length': '115',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'WZRK_G=41ddfc5bc51e4635842e85473a24d323; _ga=GA1.2.1443534606.1633492495; _hjid=9fb22319-0954-4bbe-befa-6b44733ed1ae; _fbp=fb.1.1633492495898.933719531; WIGZO_LEARNER_ID=0391f13a-ec4c-4723-848c-06b3cafa24b0; _gid=GA1.2.76989648.1634885151; customerType=existing; fbm_442881609842304=base_domain=.earnkaro.com; PAGE_UUID=0391f13a-ec4c-4723-848c-06b3cafa24b0; RID=1776687; _hjAbsoluteSessionInProgress=0; pps_referance_cookie_e4adec0a3856cae8c9d623a3ee12d9ab=5b81c416ef181aa71d87a51796f45768%7C%7C1640200105%7C%7C1635017005%7C%7C6f28f5e33f795d30dbf4e17581e380e3; _gat_UA-22268078-28=1; __insp_wid=825490797; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly9lYXJua2Fyby5jb20v; __insp_targlpt=U2hhcmUgTGluayBhbmQgTWFrZSBNb25leSBPbmxpbmUgfCBFYXJuIE1vbmV5IHdpdGggRWFybkthcm8%3D; WIGZO_DAILYACTIVE=Active; __insp_norec_sess=true; WZRK_S_466-77K-575Z=%7B%22p%22%3A2%2C%22s%22%3A1635016105%2C%22t%22%3A1635016109%7D; __insp_slim=1635016109214; X-PPS-Status=signed',
        'origin': 'https://earnkaro.com',
        'referer': 'https://earnkaro.com/create-earn-link',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    payload = {
        'deallink': datalink,
        'responseMsg': ''
    }

    data = requests.post("https://earnkaro.com/create-earn-link",
                         headers=headers, data=payload)
    links = findAllLinks(data.text)
    for lnk in links:
        if "https://ekaro.in" in lnk[0]:
            isEkaroAffiliationURLCreated = 1
            file.write("Ekaro Status: Link Generated")
            url = lnk[0]
    if isEkaroAffiliationURLCreated == 0:
        file.write("Ekaro Status: Link Not Generated\n")
    file.write("Ekaro Link: {}".format(url))
    return url


async def main():
    entity1 = await client.get_entity("teeeeeeesttttttttnmcfcnm")
    entity2 = await client.get_entity("testttttttttttt10")
    # entity3 = await client.get_entity("teeeeeeesttttttttnmcfcnm")
    # entity4 = await client.get_entity("testttttttttttt10")
    # entity5 = await client.get_entity("teeeeeeesttttttttnmcfcnm")
    # entity6 = await client.get_entity("testttttttttttt10")
    # entity7 = await client.get_entity("teeeeeeesttttttttnmcfcnm")
    # entity8 = await client.get_entity("testttttttttttt10")
    # entity9 = await client.get_entity("teeeeeeesttttttttnmcfcnm")
    # entity10 = await client.get_entity("testttttttttttt10")
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
                    "\n\noriginal lnk[0]: {}\nUnshortened link {}\n".format(lnk[0], url))
                if "instagram.com" in url or "instagram.com" in lnk[0] or "youtube.com" in url or "telegram" in url or "telegram" in lnk[0] or "t.me" in lnk[0] or "kooltech.co.in" in lnk[0] or "offerzonelootdeals.com" in lnk[0]:
                    if "https://t.me" in lnk[0] or "telegram" in url or "telegram" in lnk[0]:
                        text = text.replace(
                            lnk[0], "TELEGRAM_LINK_HERE")
                    else:
                        text = text.replace(lnk[0], '')
                    count = count - 1
                    event.message.text = text
                url = checkAndUpdateLinkRedirectURL(url, file)
                file.write("final url: {}\n".format(url))
                if url is not None and len(url) > 0:
                    # and url.find("affiliates.sankmo.com") == -1:
                    urlParts = url.split("?")
                    if url.find("affiliates.sankmo.com") == -1 and urlParts[0] in oldURLs:
                        print("---Already Posted----", urlParts[0])
                        file.write("Already Posted: {}\n".format(urlParts[0]))
                    else:
                        url = checkAndGenerate3rdPartyAffiliateLink(
                            url, urlParts[0], file)
                        event.message.text = changeLinkID(
                            url, lnk[0], event.message.text)
                        oldURLs.append(urlParts[0])
                        notPosted = notPosted + 1
                        if len(oldURLs) == 10000:
                            oldURLs.pop()
                    print(len(oldURLs))
                    file.write("oldURLs: {}\n".format(oldURLs))
            if count > 0 and notPosted > 0:
                event.message.text = removeOriginalSources(event.message.text)
                text = event.message.text
                event.message.text = text.replace(
                    "TELEGRAM_LINK_HERE", "https://t.me/thetestingphase")
                await client.send_message(entity=entity1, message=event.message)
                event.message.text = text.replace(
                    "TELEGRAM_LINK_HERE", "https://t.me/thetestingphase")
                await client.send_message(entity=entity2, message=event.message)
                # event.message.text = text.replace(
                #     "TELEGRAM_LINK_HERE", "https://t.me/thetestingphase")
                # await client.send_message(entity=entity3, message=event.message)
                # event.message.text = text.replace(
                #     "TELEGRAM_LINK_HERE", "https://t.me/thetestingphase")
                # await client.send_message(entity=entity4, message=event.message)
                # event.message.text = text.replace(
                #     "TELEGRAM_LINK_HERE", "https://t.me/thetestingphase")
                # await client.send_message(entity=entity5, message=event.message)
                # event.message.text = text.replace(
                #     "TELEGRAM_LINK_HERE", "https://t.me/thetestingphase")
                # await client.send_message(entity=entity6, message=event.message)
                # event.message.text = text.replace(
                #     "TELEGRAM_LINK_HERE", "https://t.me/thetestingphase")
                # await client.send_message(entity=entity7, message=event.message)
                # event.message.text = text.replace(
                #     "TELEGRAM_LINK_HERE", "https://t.me/thetestingphase")
                # await client.send_message(entity=entity8, message=event.message)
                # event.message.text = text.replace(
                #     "TELEGRAM_LINK_HERE", "https://t.me/thetestingphase")
                # await client.send_message(entity=entity9, message=event.message)
                # event.message.text = text.replace(
                #     "TELEGRAM_LINK_HERE", "https://t.me/thetestingphase")
                # await client.send_message(entity=entity10, message=event.message)
                file.write("<== Posted ==>\n")
            else:
                print(text)
                file.write("\ntext => {}\n".format(text))
                file.write("Count: {} and notPosted: {}\n".format(
                    count, notPosted))
                file.write("<== Not Posted ==>\n")
            file.write("--------------------\n\n\n")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
client.run_until_disconnected()
