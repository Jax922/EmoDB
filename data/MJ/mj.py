

import json
import os
import sys
import time
from tqdm import tqdm
import requests
from datetime import datetime, timezone
from PIL import Image
import re   


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils as UTILS
import db as DB
import log as LOG

save_path = "/Users/shedong/Documents/AIGC-image/MJ/"

def load_json_data(json_path):
    json_data = {}
    with open(json_path, 'r') as f:
        data = json.load(f)
        # 将每个MJ_data.json中的图片ID与图片信息映射
        for item in data:
            image_id = extract_image_id(item['full_img_url'])
            json_data[image_id] = item
    return json_data


def check_image_id_exist(image_id, json_data):
    if image_id in json_data:
        return True
    return False

def extract_image_id(url):
    if re.search(r'\(\d+\)', url):
        print("重复文件")
        return None
    match = re.search(r'([a-f0-9\-]{36})', url)  # 匹配UUID格式
    if match:
        return match.group(1)
    return None  # 如果没有找到匹配，返回None

def compress_image(image_path, output_path, quality=70):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.save(output_path, format="JPEG", quality=quality, optimize=True)

def convert_to_timestamp(time_str):
    # 假设年份为 2024年，拼接到字符串前面
    time_str_with_year = f"2024 {time_str}"
    
    # 解析字符串为 datetime 对象
    time_obj = datetime.strptime(time_str_with_year, '%Y %d %b, %I:%M %p')
    
    # 返回时间戳（秒级）
    return int(time_obj.timestamp())

def get_image_dimensions(image_path):
    # 打开图片
    with Image.open(image_path) as img:
        # 获取宽度和高度
        width, height = img.size
    return width, height

def handle_main(mj_dir):
    abs_mj_dir = os.path.join(save_path, mj_dir)
    json_path = os.path.join(abs_mj_dir, "MJ_data.json")
    imgs_dir = os.path.join(abs_mj_dir, "img")
    small_imgs_dir = os.path.join(abs_mj_dir, "small_img")

    if not os.path.exists(small_imgs_dir):
        os.makedirs(small_imgs_dir)
    
    json_data = load_json_data(json_path)
    print(f"json_data length: {len(json_data)}")
    print(f"json_data  first two keys: {list(json_data.keys())[:2]}")

    for file in os.listdir(imgs_dir):
        image_id = extract_image_id(file)
        print(f"image_id: {image_id}")
        is_existed = check_image_id_exist(image_id, json_data)
        if image_id:
            image_path = os.path.join(imgs_dir, file)
            image_hash = UTILS.get_image_hash(image_path)
            suffix = file.split('.')[-1]
            image_name = f'{image_hash}.{suffix}'
            output_path = os.path.join(small_imgs_dir, image_name)
            compress_image(image_path, output_path)
            print(f"Compressed image: {file}")
            print(f"Compressed image path: {output_path}")
            image_type = suffix
            model = "midjourney"
            width, height = get_image_dimensions(image_path)
            image_url = ""
            small_image_url = ""
            prompt_text = ""
            timestamp = ""
            if is_existed:
                image_url = json_data[image_id]['full_img_url']
                small_image_url = json_data[image_id]['small_img_url']
                prompt_text = json_data[image_id]['prompt_text']
                timestamp = convert_to_timestamp(json_data[image_id]['create_time'])
            
            document = {
                'image_name': image_name,
                'image_url': image_url,
                'small_image_url': small_image_url,
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

            print(f"Save document to DB: {document}")
            save_db(document)


def save_db(document):
    LOG.log_message(f"Save document to DB: {document}", level='info')
    imgDB = DB.MongoDBHandler()
    imgDB.insert_document(document, collection_name="MJ_website_images")
    time.sleep(0.1)
    print("Save to DB successfully")

if __name__ == "__main__":
    handle_main("MJ-1")
    handle_main("MJ-2")
    handle_main("MJ-3")
    handle_main("MJ-4")
    handle_main("MJ-5")
    


