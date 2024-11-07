import sys
import os
import time
from tqdm import tqdm
import requests
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils as UTILS
import db as DB
import log as LOG

request_interval = 1
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
    'sessionid': 'sjg9snhrg5e5iq3vid0wfheze7sjhiep',  # 从浏览器中复制
    'csrftoken': 'ZkbhGwXNU6aZVbV7QyKR0jbByKhvP4xg',  # 从浏览器中复制
    'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwODE0NDI2LCJpYXQiOjE3MzA4MTI2MjYsImp0aSI6ImI5NjA1NDQyMDU5YzQ0ZDg5YzA0MzFmOTg2MTIzZDdjIiwidXNlcl9pZCI6MTA4NTB9.W_UhEClF-o5McjYQiwH4MeIpis_fNVsS3syNl53cY_U'  # 从浏览器中复制
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
# response = session.post(login_url, headers=headers, cookies=cookies, json=data)


# 检查登录是否成功
# if response.status_code == 200:
#     print('Login successful')
#     print('Cookies:', session.cookies)
# else:
#     print('Login failed', response.status_code)
#     print('Response:', response.text)  # 查看响应内容，诊断错误
#     print('Response:', response)



############## laprompt.com API ##############
all_results = []
# next_url = "http://api.laprompt.com/api/v1/premium/prompts/?ai_model_type=2&cursor=cj0xJnA9JTVCJTIyOTY5JTIyJTJDKyUyMjEwMjQlMjIlNUQ%3D&page_size=16"
next_url = "http://api.laprompt.com/api/v1/premium/prompts/?ai_model_type=2&cursor=cD0lNUIlMjIzMTYlMjIlMkMrJTIyMzIwJTIyJTVE&page_size=16"

# default_headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
#         'Accept': '*/*',
#         'Accept-Language': 'en,en-US;q=0.9',
#         'Origin': 'https://laprompt.com',
#         'Referer': 'https://laprompt.com/'

#     }

default_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en,en-US;q=0.9',
    'Cache-Control': 'no-cache',
    'Cookie': '_gcl_au=1.1.162804458.1730786415.1384332914.1730812607.1730813184; access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwODE0OTg4LCJpYXQiOjE3MzA4MTMxODgsImp0aSI6ImNlMTQ5M2NhNzUxYzRhZGI5OTU2YmQ0ZTRjNWM3YzFjIiwidXNlcl9pZCI6MTA4NTB9.DtsFfMl8ZMKOwdGVI3p4RMaHIZxLfS3-0FBQ70Gkwhs; refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjYyNzU4OCwiaWF0IjoxNzMwODEzMTg4LCJqdGkiOiI3NTBhMzNmMWVkNGM0YjcwOTViMmRmMmRmZjZhMDM3ZiIsInVzZXJfaWQiOjEwODUwfQ.UC4MoStlRqcxbRsfReHjz7O1A-YnZ0JXEULOJ1_buBk; csrftoken=JYZRNKqs5FqMcJyQZqyFWr921zr2f8pS; sessionid=pmpgulxnlq8sf3pafrn7iyrwaccyzd43',
    'Origin': 'https://laprompt.com',
    'Pragma': 'no-cache',
    'Referer': 'https://laprompt.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
}

prompt_headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en,en-US;q=0.9",
    "cache-control": "no-cache",
    "cookie": "_gcl_au=1.1.162804458.1730786415.1384332914.1730812607.1730813184; csrftoken=JYZRNKqs5FqMcJyQZqyFWr921zr2f8pS; sessionid=pmpgulxnlq8sf3pafrn7iyrwaccyzd43; access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwODIyNzI3LCJpYXQiOjE3MzA4MTkwMDgsImp0aSI6IjdkY2ExYjg3MmM5ZTQ5OWE4YzFhMjlhYzYyNDMyZDA1IiwidXNlcl9pZCI6MTA4NTB9.a12tr8rsBn6eyKh04AcsVuGZvf8o7nt2sgjEXWZvBXs; refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjYzNTMyNywiaWF0IjoxNzMwODIwOTI3LCJqdGkiOiJkNGE2ZWJjNDVkZTk0MjA5YTUyZjZjZmI1M2JlMmY0YiIsInVzZXJfaWQiOjEwODUwfQ.DKrtY8gQ9z929PxTd4kLTOfEM0GrJdQrbr95NmUqum4",
    "origin": "https://laprompt.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://laprompt.com/",
    "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}
# refresh token
refresh_token_val = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjYzNzM1NywiaWF0IjoxNzMwODIyOTU3LCJqdGkiOiJiZDI4NWY2ZTJlY2I0MzI4YmEyZmI1M2RjZjg1NWNhOCIsInVzZXJfaWQiOjEwODUwfQ.Z_yxtqf7nfmom6ubAeVc7OkIRnj6y9JXocxJVs78mNE'
refresh_time = 0

def refresh_token():
    # 刷新 token 请求
    url = "https://api.laprompt.com/api/v1/auth/token/refresh/"
    headers = {
        'Content-Type': 'application/json'
    }
    cookies = {
        'refresh_token': refresh_token_val
    }

    # 发起请求
    res = requests.post(url, headers=headers, cookies=cookies)
    # res = UT(url, headers=headers, cookies=cookies, method='POST')

    oringinal_cookie = prompt_headers['cookie']
    if res.status_code == 200:
        res = res.json()
        new_access_token = res['access']
        access_expiration = res['access_expiration']
        refresh_time = datetime.strptime(access_expiration, "%Y-%m-%dT%H:%M:%S.%fZ")

        prompt_headers['cookie'] = f'access_token={new_access_token}; ' + "; ".join([item for item in oringinal_cookie.split(';') if 'access_token' not in item])
        LOG.log_message(f"New access token: {new_access_token}", level='info')
    else:
        LOG.log_message("Failed to refresh token", level='error')
        return None



# prmopt_url = "https://api.laprompt.com/api/v1/premium/prompts/1085/view"
def generate_prompt_url(image_id):
    base_url = "https://api.laprompt.com/api/v1/premium/prompts/"
    prompt_url = f"{base_url}{image_id}/view"
    return prompt_url

def get_prompt_info(prompt_url):

    current_time = datetime.now(timezone.utc).timestamp()
    if current_time > refresh_time:
        refresh_token()
    response = UTILS.send_request(prompt_url, headers=prompt_headers)
    if response is None:
        refresh_token()
        time.sleep(prompt_interval)
        response = UTILS.send_request(prompt_url, headers=prompt_headers)

    if response is None:
        return None

    return response['prompt_text']
##################################################

save_dir = os.path.join(UTILS.get_save_dir(), "laprompt")
print(f"Save dir: {save_dir}")
UTILS.create_save_dir(save_dir)

n = 1
total_imgs = 0

LOG.log_message("Start downloading images from laprompt.com", level='info')
while next_url:
    response = UTILS.send_request(next_url, headers=default_headers)
    all_results = response['results']
    if 'next' in response:
        next_url = response['next']
    else:
        next_url = None
    LOG.log_message(f"Next URL: {next_url}", level='info')
    n += 1

    LOG.log_message(f"Total imgs: {len(all_results)}", level='info')

    imgDB = DB.MongoDBHandler()

    refresh_token()

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
        if res['id']:
            prompt_url = generate_prompt_url(res['id'])
            prompt_text = get_prompt_info(prompt_url)
            if prompt_text is None:
                prompt_text = "N/A"
        else:
            prompt_text = "N/A"
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


