
# https://civitai.com/

import sys
import os
import time
from tqdm import tqdm
import requests
from datetime import datetime, timezone
import urllib.parse
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils as UTILS
import db as DB
import log as LOG

request_interval = 0.1

# url: https://civitai.com/api/trpc/image.getInfinite?input={%22json%22:{%22useIndex%22:true,%22period%22:%22AllTime%22,%22sort%22:%22Oldest%22,%22types%22:[%22image%22],%22browsingLevel%22:1,%22include%22:[],%22cursor%22:null},%22meta%22:{%22values%22:{%22cursor%22:[%22undefined%22]}}}
base_url = "https://civitai.com/api/trpc/image.getInfinite?"
params = {
    "input": {
        "json": {
            "useIndex": True,
            "period": "AllTime",
            "sort": "Newest",
            "types": ["image"],
            "browsingLevel": 1,
            "include": [],
            "cursor": None
        },
        "meta": {
            "values": {
                "cursor": ["undefined"]
            }
        }
    }
}

# print(json.dumps(params["input"]))

def get_full_url(base_url, params):
    params_json = json.dumps(params["input"])

    full_url = base_url + "input=" + params_json
    return full_url

def download_image(img_url, img_name, model):
    # print(f"Downloading image: {img_name}")
    # print(f"Model: {model}")
    save_path = os.path.join(UTILS.get_save_dir(), "civitai")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_path = os.path.join(save_path + "/"+ img_name)

    try:
        response = requests.get(img_url)
    except Exception as e:
        LOG.log_message(f"Failed to download image. Error: {e}", level='error')
        return False

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        LOG.log_message(f"Image successfully downloaded: {save_path}", level='info')
    else:
        LOG.log_message(f"Failed to download image. Status code: {response.status_code}", level='error')
        return False

    return save_path

def get_prompt_text(img_id):
    if type(img_id) != str:
        img_id = str(img_id)
    base_url = 'https://civitai.com/api/trpc/image.getGenerationData?input={"json":{"id":image_id}}'
    url = base_url.replace("image_id", img_id)


    response = UTILS.send_request(url, method='GET', is_print=False)
    prompt_text = "N/A"
    if response:
        # prompt_text = response["result"]["data"]["json"]["meta"]["prompt"] if "prompt" in response["result"]["data"]["json"]["meta"] else "N/A"
        if response["result"]:
            if response["result"]["data"]:
                if response["result"]["data"]["json"]:
                    if response["result"]["data"]["json"]["meta"]:
                        if "prompt" in response["result"]["data"]["json"]["meta"]:
                            prompt_text = response["result"]["data"]["json"]["meta"]["prompt"]

    return prompt_text



# LOG.log_message(f"Requesting images from {base_url}", level='info')
# full_url = get_full_url(base_url, params)
# LOG.log_message(f"First Request, Full URL: {full_url}", level='info')
# response = UTILS.send_request(get_full_url(base_url, params), method='GET')

# # handle response
# next_cursor = response["result"]["data"]["json"]["nextCursor"] if response["result"]["data"]["json"]["nextCursor"] else None
# LOG.log_message(f"Next cursor: {next_cursor}", level='info')
# items = response["result"]["data"]["json"]["items"]
# LOG.log_message(f"Total items: {len(items)}", level='info')
# LOG.log_message(f"Start downloading images...", level='info')

def parse_data(items):
    for item in tqdm(items):
        id = item["url"]
        model = item["baseModel"] if item["baseModel"] else "unknown"
        create_time = item["publishedAt"]
        # 解析 ISO 格式时间为 datetime 对象
        dt_object = datetime.strptime(create_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        timestamp = dt_object.timestamp()

        down_url_base = "https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/image_id/original=true.jpeg"
        image_url = down_url_base.replace("image_id", id)
        image_name = UTILS.get_image_uuid() + ".jpeg"

        image_path = download_image(image_url, image_name, model)
        if not image_path: # that means download failed, NSFW image
            continue

        image_hash = UTILS.get_image_hash(image_path)
        image_type = "jpeg"
        width = item["width"]
        height = item["height"]
        prompt_text = get_prompt_text(item["id"])

        document = {
                'image_name': image_name,
                'image_url': image_url,
                'image_hash': image_hash,
                'image_type': image_type,
                'image_path': image_path,
                'ai_model': model,
                'timestamp': timestamp,
                'source': 'civitai.com',
                'prmopt_text': prompt_text,
                'width': width,
                'height': height
        }
        LOG.log_message(f"Save document to DB: {document}", level='info')
        imgDB = DB.MongoDBHandler()
        imgDB.insert_document(document, collection_name="civitai_images")
        # time.sleep(request_interval)

# parse first response
# parse_data(items)


# img_counts = len(items)
img_counts = 0
max_round = 50
next_cursor = "50|1731143460000"

while next_cursor and (max_round>0):
    print(f"Round: {max_round}")
    params["input"]["json"]["cursor"] = next_cursor
    full_url = get_full_url(base_url, params)
    LOG.log_message(f"Request, Full URL: {full_url}", level='info')
    response = UTILS.send_request(get_full_url(base_url, params), method='GET')
    next_cursor = response["result"]["data"]["json"]["nextCursor"] if response and response["result"]["data"]["json"]["nextCursor"] else None
    items = []
    # items = response["result"]["data"]["json"]["items"]
    if "result" in response:
        if "data" in response["result"]:
            if "json" in response["result"]["data"]:
                if "items" in response["result"]["data"]["json"]:
                    items = response["result"]["data"]["json"]["items"]

    LOG.log_message(f"Next cursor: {next_cursor}", level='info')
    LOG.log_message(f"max_round_current: {max_round}", level='info')
    img_counts += len(items)
    LOG.log_message(f"Total images: {img_counts}", level='info')
    print(f"Total images: {img_counts}")
    max_round -= 1
    parse_data(items)



