import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl import functions, types
import requests
from urllib.parse import unquote
import json

api_id = 6487373
api_hash = '700f3b0513f9a1a321b28d4eed4a4140'
channel_usernames = ["kooltech007", "Offerzone_deals", "Loot_Offers_Dealss", "Rishavtechnical", "freekaamaalindia", "loottimes", "bigtricksin", "zingoy","Offerzone_Tricks_1","offerzone_Offerzone_Tricks",
                     "freekamaal7", "gopaisadeals", "loots_point", "Deals_Point", "IrfanTechHelper", "CKoffers", "rapid_loot_deal", "LootTalks", "ArifAnsar", "tech25withaman","PremiumDealsX","roobaiofficial"]
client = TelegramClient("session_name", api_id, api_hash).start()
oldURLs = []


def unshorten_url(url):
    response = requests.get(url)
    return response.url


def isNotFlipkartQuiz(text):
    return text.lower().find("ladies and gentlemen") == -1 and text.lower().find("kya bolti public") == -1 and text.lower().find("daam sahi hai") == -1 and text.lower().find("fake or not") == -1 and text.lower().find("fake or not fake") == -1 and text.lower().find("khel paheliyon ka") == -1 and text.lower().find("daam sahi hai") == -1 and text.lower().find("sirf ek minute") == -1


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
    # updatedUrl = unshortenedUrl
    # headers = {
    #     "accept": "application/json, text/javascript, */*; q=0.01",
    #     "accept-encoding": "gzip, deflate, br",
    #     "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    #     "content-length": "47",
    #     "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    #     "cookie": "_xsrf=00d260fbf3f64b9bb158f8dcc4069c0b; anon_u=cHN1X19iZDk2MWFiYS1jNzQyLTRlZDgtOGQxMi02OGI2NzhiMDhjNzg=|1662755201|64a101c4c96477321346e343172717cfef759c5a; _gcl_au=1.1.989150232.1662755203; optimizelyEndUserId=oeu1662755203014r0.6117418209273864; _gid=GA1.2.797823653.1662755203; _sp_ses.741f=*; _ga_567GCTL9BB=GS1.1.1662755203.1.1.1662755204.59.0.0; _ga=GA1.1.318024360.1662755203; _fbp=fb.1.1662755205479.628329990; _hjSessionUser_3068185=eyJpZCI6ImQ2ODFlOTExLTI4MDgtNWQzZS04ODhhLTk0ODNiOThjODBiYSIsImNyZWF0ZWQiOjE2NjI3NTUyMDU2NzMsImV4aXN0aW5nIjpmYWxzZX0=; _hjFirstSeen=1; _hjIncludedInSessionSample=0; _hjSession_3068185=eyJpZCI6IjQxMWFkNTg5LTlmMDYtNDkwZS1hMTI2LTFkMjI1N2UxODRlZCIsImNyZWF0ZWQiOjE2NjI3NTUyMDU4MzgsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _sp_id.741f=70e76ff1-309a-415e-8238-c553cf108a5f.1662755204.1.1662755245.1662755204.86dd5ad9-962c-426c-957c-a1f8a3b47974",
    #     "origin": "https://bitly.com",
    #     "referer": "https://bitly.com/pages/home/v1",
    #     "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-ch-ua-platform": '"macOS"',
    #     "sec-fetch-dest": "empty",
    #     "sec-fetch-mode": "cors",
    #     "sec-fetch-site": "same-origin",
    #     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    #     "x-requested-with": "XMLHttpRequest",
    #     "x-xsrftoken": "00d260fbf3f64b9bb158f8dcc4069c0b",
    # }
    # payload = {
    #     'url': unshortenedUrl
    # }

    # data = requests.post("https://bitly.com/data/anon_shorten",
    #                      headers=headers, data=payload)
    # if data.status_code == 200:
    #     print("-----unshortenedUrl-----", unshortenedUrl)
    #     print("-----textUrl-----", textUrl)
    #     updatedUrl = json.loads(data.text)['data']['link']
    #     text = text.replace(textUrl, updatedUrl)
    #     print("-----updatedUrl-----", updatedUrl)
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
    entity1 = await client.get_entity("shopping_loot_offers_live_deals")
    entity2 = await client.get_entity("deallootere")
    entity3 = await client.get_entity("dealchor")
    entity4 = await client.get_entity("freedealszone")
    entity5 = await client.get_entity("freeshoppingzone")
    entity6 = await client.get_entity("offers_flipkart_amazon_deals")
    notposteddeals = await client.get_entity("notposted")
    print("Started Listening to the messages")

    @client.on(events.NewMessage(chats=channel_usernames))
    async def main(event):
        text = event.message.text
        links = findAllLinks(text)
        count = len(links)
        file = open("myfile.txt", "a", encoding="utf-8")
        urlFile = open("allurls.txt", "a", encoding="utf-8")
        if isNotFlipkartQuiz(text):
            notPosted = 0
            for lnk in links:
                url = unshorten_url(lnk[0])
                urlFile.write("{}\n".format(url))
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
                    "TELEGRAM_LINK_HERE", "https://t.me/shopping_loot_offers_live_deals")
                await client.send_message(entity=entity1, message=event.message)
                event.message.text = text.replace(
                    "TELEGRAM_LINK_HERE", "https://t.me/deallootere")
                await client.send_message(entity=entity2, message=event.message)
                event.message.text = text.replace(
                    "TELEGRAM_LINK_HERE", "https://t.me/dealchor")
                await client.send_message(entity=entity3, message=event.message)
                event.message.text = text.replace(
                    "TELEGRAM_LINK_HERE", "https://t.me/freedealszone")
                await client.send_message(entity=entity4, message=event.message)
                event.message.text = text.replace(
                    "TELEGRAM_LINK_HERE", "https://t.me/freeshoppingzone")
                await client.send_message(entity=entity5, message=event.message)
                event.message.text = text.replace(
                    "TELEGRAM_LINK_HERE", "https://t.me/offers_flipkart_amazon_deals")
                await client.send_message(entity=entity6, message=event.message)
                file.write("<== Posted ==>\n")
            else:
                event.message.text = text
                await client.send_message(entity=notposteddeals, message=event.message)
                print(text)
                file.write("\ntext => {}\n".format(text))
                file.write("Count: {} and notPosted: {}\n".format(
                    count, notPosted))
                file.write("<== Not Posted ==>\n")
            file.write("--------------------\n\n\n")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
client.run_until_disconnected()
