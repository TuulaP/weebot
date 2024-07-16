
# Goal , post a random cat clipping to Mastodon as a bot.

import requests
import os
from dotenv import load_dotenv

DEBUG = 0

api_base_url = 'https://botsin.space/api/v1/statuses'


def sendSimpleToot (tootText="TEST234", language = "fi", visibility = "public"):

    load_dotenv()
    APPID = os.getenv('APPID')
    APPSECRET = os.getenv('APPSECRET')
    APPTOKEN = os.getenv('APPTOKEN')
    BEARERTOKEN = os.getenv('BEARERTOKEN')

    if DEBUG > 0:
        print("BEARERTOK: ", BEARERTOKEN)

    print(tootText)

    headers = {
        'Authorization' : 'Bearer %s' % (BEARERTOKEN),
        'Accept' : 'application/json'
    }


    payload = {
        "status" : tootText ,
        "language" : language,
        "media_ids[]"  : [],
        "visibility" : visibility

    }
    
    if BEARERTOKEN is not None:
        response = requests.post(
            api_base_url,
            data = payload,
            headers = headers
        )
    else:
        print("ERR, conf file missing.")
    

    if (DEBUG > 0):
        print(response.json)
        #print(requests.get(url, headers=headers))
        print("-------")
        print(response)
        print(response.status_code)
        print(response.headers)




if __name__ == "__main__":

    sendSimpleToot("test1")

    print("Done!")
