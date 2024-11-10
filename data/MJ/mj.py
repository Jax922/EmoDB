

import json
import os
import sys
import time
from tqdm import tqdm
import requests
from datetime import datetime, timezone


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils as UTILS
import db as DB
import log as LOG

save_path = "/home/pci/dong/AIGC-image/mj/"

# read the raw json data from ./data/data_2024-11-10 11:56:26.json
def read_data():
    with open(os.path.join(os.path.dirname(__file__), 'data_2024-11-10 11:56:26.json')) as f:
        data = json.load(f)
    return data

# download the images from the data
def fetch_image(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Referer": "https://dalle2.gallery/",
        "If-Modified-Since": "Sat, 09 Nov 2024 07:26:34 GMT",
        "Sec-CH-UA": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "Sec-CH-UA-Arch": '"x86"',
        "Sec-CH-UA-Bitness": '"64"',
        "Sec-CH-UA-Full-Version": '"130.0.6723.91"',
        "Sec-CH-UA-Full-Version-List": '"Chromium";v="130.0.6723.91", "Google Chrome";v="130.0.6723.91", "Not?A_Brand";v="99.0.0.0"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": "Linux",
        "Sec-CH-UA-Platform-Version": "6.5.0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }

    # 如果需要使用 Cookie，请将其复制到此处
    cookies = {
        "AMP_MKTG_437c42b22c": "JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tLmhrJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tLmhrJTIyJTdE",
        "_gcl_au": "1.1.1498244188.1730992371",
        "_ga": "GA1.1.1613374330.1730992371",
        "AMP_437c42b22c": "JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI3NmVlN2I0ZC1iODUwLTQyN2YtYmFlYS1mMTIzNTIwNzA1MjMlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMxMDYzMDkzNjU1JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczMTA2Mzc1MjU1OSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTM1JTdE",
        "cf_clearance": "3ryjjX9SVXqMK5FBlKuei_W_QXx6.wQW.JvKCCntqNc-1731063753-1.2.1.1-YR_lEuXUGehkau9aPRKg7QKZkZHqBCv7FdSdGSpjAGxHFv.UVRkXuDRVexCfnx8YIJVvY9ziK1MLSenxXae8oGes4ciOi_QY.tEC4TVMzFT3spNoPTJI6E4olFy4uxlUaBIOrbn8oqUXVwv8e8ijWRtdYLtTzCYP5t43mSt6uOXo9rgTYC0ctXTmazHX_zV3oe7iNwJBm2CTCYZFuQDVCpqdbM6J3nib7cq7teaFATCPzDX_sSlgLzD_84r77FMFHX9UBKsDoWE57YPnSYgVOvos0d7TPhTrzhVQH3sXakVKH7FpyJewVmae2lliAhjDMqT4nOfgmpdWYwLqWQGNRMfEskRsAY94G1_bz5MbXc9ZZEqqqgdbOZ1PKPUuhwrn",
        "_ga_Q0DQ5L7K0D": "GS1.1.1731211155.4.0.1731211155.0.0.0",
        "__cf_bm": "GgykjJnMZjtISduj4rsbKbjZM7lQfVQiuzFkn4aTD5k-1731211717-1.0.1.1-7Cja.ZbDkuaayFlJS7ZrtH8cYkmsIV6oNxItXqNW3ydHhpapeIwOIpj66Iqx.YYShDLqlZMDdIJ4VP6tXXJwsw",
    }
    res = requests.get(url, headers=headers, cookies=cookies)
    if res.status_code == 200:
        with open(save_path + "image.jpg", 'wb') as f:
            f.write(res.content)
        LOG.log_message(f"Image successfully downloaded: {save_path}", level='info')
    else:
        print(f"Failed to download image. Status code: {res.status_code}")
        # print(f"Response: {res.text}")  
        LOG.log_message(f"Failed to download image. Status code: {res.status_code}", level='error')

fetch_image("https://cdn.midjourney.com/00159e23-f228-40e1-92d7-6be5343fe8d9/0_0_384_N.webp?method=shortest&qst=6&quality=15")
