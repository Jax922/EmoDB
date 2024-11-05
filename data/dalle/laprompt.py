import sys
import os
import time
from tqdm import tqdm
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils as UTILS
import db as DB
import log as LOG

request_interval = 5 
prompt_interval = 2



def download_image(image_url, save_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': 'https://laprompt.com/gallery/text-to-image/dalle-3',
        'Accept-Encoding': 'gzip, deflate, br, zstd'
    }

    response = requests.get(image_url, headers=headers)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        LOG.log_message(f"Image successfully downloaded: {save_path}", level='info')
    else:
        LOG.log_message(f"Failed to download image. Status code: {response.status_code}", level='error')

###### login
# 设置需要的 cookies 和 headers
cookies = {
    'sessionid': 'sh97y522749rr2gnf2mbe8b55x7hipbd',  # 从浏览器中复制
    'csrftoken': '7Iq9hAoKUEjhpiOXMkY3yJgJVsmpydjA',  # 从浏览器中复制
    'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwNzkxNzc4LCJpYXQiOjE3MzA3ODk5NzgsImp0aSI6IjFhOTQxZTc3NjJlNjQ5YjVhMGM4MzE1ZjNiZWE5YjhlIiwidXNlcl9pZCI6MTA4NTB9.FAmwzgzA0YaTpNl9tOS1jX4IQ2P37qEQOs4u-OXwSgg',  # 从浏览器中复制
}

headers = {
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Origin': 'https://laprompt.com',
    'Referer': 'https://laprompt.com/',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
}

# 登录的URL
login_url = 'https://api.laprompt.com/api/v1/auth/login/'

# 设置登录的请求体（例如用户名和密码）
data = {
    'username': 'dshe922@gmail.com ',  # 你需要替换成实际的用户名
    'password': 'Jax919922.'   # 你需要替换成实际的密码
}

# 启用会话，保持 cookies
session = requests.Session()

# 发送 POST 请求进行登录
response = session.post(login_url, headers=headers, cookies=cookies, json=data)


# 检查登录是否成功
if response.status_code == 200:
    print('Login successful')
    print('Cookies:', session.cookies)
else:
    print('Login failed', response.status_code)
    print('Response:', response.text)  # 查看响应内容，诊断错误
    print('Response:', response)



############## laprompt.com API ##############
all_results = []
next_url = "http://api.laprompt.com/api/v1/premium/prompts/?ai_model_type=2&cursor=cj0xJnA9JTVCJTIyOTY5JTIyJTJDKyUyMjEwMjQlMjIlNUQ%3D&page_size=16"

default_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.9',
        'Origin': 'https://laprompt.com',
        'Referer': 'https://laprompt.com/'
    }

# prmopt_url = "https://api.laprompt.com/api/v1/premium/prompts/1085/view"
def generate_prompt_url(image_id):
    base_url = "https://api.laprompt.com/api/v1/premium/prompts/"
    prompt_url = f"{base_url}{image_id}/view"
    return prompt_url

def get_prompt_info(prompt_url):
    response = UTILS.send_request(prompt_url, headers=default_headers)
    return response['prompt_text']
##################################################

save_dir = os.path.join(UTILS.get_save_dir(), "laprompt")
print(f"Save dir: {save_dir}")
UTILS.create_save_dir(save_dir)

n = 2
total_imgs = 0

LOG.log_message("Start downloading images from laprompt.com", level='info')
while n<2:
    response = UTILS.send_request(next_url, headers=default_headers)
    all_results = response['results']
    next_url = response['next']
    LOG.log_message(f"Next URL: {next_url}", level='info')
    n += 1

    LOG.log_message(f"Total imgs: {len(all_results)}", level='info')

    imgDB = DB.MongoDBHandler()

    for res in tqdm(all_results):
        image_counts = len(res['images'])
        image_url = res['images'][image_counts-1]["image"]
        image_type = image_url.split('.')[-1]
        image_name = UTILS.get_image_uuid() + '.' + image_type
        image_path = os.path.join(save_dir+"/"+image_name)
        download_image(image_url, image_path)
        image_hash = UTILS.get_image_hash(image_path)
        AI_model = res['ai_model_name']
        timestamp = res['created_at']
        prompt_url = generate_prompt_url(res['id'])
        prompt_text = get_prompt_info(prompt_url)
        document = {
            'image_name': image_name,
            'image_url': image_url,
            'image_hash': image_hash,
            'image_type': image_type,
            'image_path': image_path,
            'ai_model': AI_model,
            'timestamp': timestamp,
            'source': 'laprompt.com',
            'prmopt_text': prompt_text
        }
        # documents.append(document
        imgDB.insert_document(document)
        time.sleep(request_interval)
    imgDB.close()
    total_imgs += len(all_results)


LOG.log_message(f"Total images downloaded: {total_imgs}", level='info')


