#post request python
import os

import requests

def get_leclerc(data):
    url = 'https://www.e.leclerc/api/rest/infomil-bridge/tdm/ticket/detail'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
    }

    #env
    didomi_token = os.getenv("DIDOMI_TOKEN")

    cookies = {
        "didomi_token": didomi_token
    }

    response = requests.post(url, headers=headers, json=data, cookies=cookies)

    if response.status_code < 200 or response.status_code >= 300:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

    s = response.json()["html"]
    return s