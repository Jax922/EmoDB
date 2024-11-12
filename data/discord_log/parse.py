from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import os
import imagehash
from datetime import datetime
from tqdm import tqdm

HTML_DIR = "/home/pci/dong/discord-log"
SAVE_DIR = "/home/pci/dong/AI-images/discord-log"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "If-Modified-Since": "Thu, 09 May 2024 19:11:46 GMT",
    "Cookie": "_cfuvid=BjNmDeaZ90aaAQAd5NIr1mf4ptTw_dQz7liaklowLQo-1731414968897-0.0.1.1-604800000; __cf_bm=jW2BzEkmZZFapWOq3pL3st9A7V9ZmfK8VhQjXdu8uXk-1731416016-1.0.1.1-TYp0K3IdLLzjiFe19VigMBumysZmWSi7CsE7AwbQoRtzI9ahpf7pb9vYoTMkDCUJzB73ZMCH9632GGWMywspQw",
    "Sec-Ch-Ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Linux"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"
}

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def compress_image(img_url, save_path, create_time, prompt_text,  json_file, quality=70):
    print(f"Downloading image {img_url}")
    response = requests.get(img_url, headers=headers)
    print("response status code:", response.status_code)
    if response.status_code!= 200:
        print(f"Failed to download image {img_url}")
        return

    img = Image.open(BytesIO(response.content))
    image_hash = imagehash.average_hash(img)
    suffixed_name = img_url.split("/")[-1]
    image_name = f"{image_hash}.{suffixed_name}"
    save_path = os.path.join(save_path, image_name)

    # 设置压缩质量 (0 到 100，值越低，压缩越强)
    # quality = 70  # 可以根据需要调整
    width, height = img.size
    time_obj = datetime.strptime(create_time, "%Y/%m/%d %H:%M")

    # 转换为时间戳
    timestamp = int(time_obj.timestamp())
    # 保存压缩后的图片
    # img.save(save_path, "JPEG", quality=quality)
    print(f"Saved image to {save_path}")
    document = {
        'image_name': image_name,
        'image_url': img_url,
        'image_hash': image_hash,
        'image_type': suffixed_name,
        'image_path': save_path,
        'ai_model': "stable_diffusion",
        'timestamp': timestamp,
        'source': 'civitai.com',
        'prmopt_text': prompt_text,
        'width': width,
        'height': height
    }
    # 保存到json文件
    with open(json_file, "a") as f:
        f.write(f"{document}\n")



def parse_html_SD(html_doc, save_dir):

    json_file = os.path.join(save_dir, f"{save_dir}.json")

    dir_path = os.path.join(SAVE_DIR, save_dir)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    soup = BeautifulSoup(html_doc, 'html.parser')
    message_groups = soup.find_all('div', class_='chatlog__message-group')
    print(f"Number of message groups: {len(message_groups)}")
    n = 0
    
    for message_group in tqdm(message_groups):
        message_group_author = message_group.find('span', class_='chatlog__author')
        # print(f"Author: {message_group_author.text}")
        if "Stable Artisan" in message_group_author.text:
            attatchments = message_group.find_all('div', class_='chatlog__attachment')
            for attatchment in attatchments:
                # attatchment.find('img', class='chatlog__attachment-media')
                img = attatchment.find('img', class_='chatlog__attachment-media')
                if img:
                    
                    create_time = message_group.find('span', class_='chatlog__timestamp')
                    timestamp = create_time.find("a").text.strip()
                    
                    prompt_text = message_group.find('span', class_='chatlog__markdown-preserve')
                    text_elems = prompt_text.find_all('strong')
                    prompt_text = " ".join([elem.text for elem in text_elems])
                    print(f"Prompt text: {prompt_text}")
                    compress_image(img['src'], dir_path, timestamp, prompt_text, json_file)
                    n += 1

    print(f"Number of attatchments: {n}")

if __name__ == '__main__':
    with open(HTML_DIR + "/Stable Diffusion - Artisan - artisan-3 [1237460408651223121].html", "r") as f:
        html_doc = f.read()
        parse_html_SD(html_doc, "stable_diffusio_3")


