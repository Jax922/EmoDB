import requests
import uuid
from PIL import Image
import imagehash
import os


def send_request(url, params=None, headers=None, method='GET'):
    """
    发送HTTP请求并返回响应内容。

    :param url: 请求的URL
    :param params: 请求的参数（可选）
    :param headers: 请求头（可选）
    :param method: 请求方法（默认为'GET'）
    :return: 响应内容或None
    """
    print(f"Sending {method} request to {url}...")                          
    try:
        # 根据请求方法发送请求
        if method.upper() == 'GET':
            response = requests.get(url, params=params, headers=headers, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, json=params, headers=headers, timeout=10)
        else:
            raise ValueError("Unsupported method: {}".format(method))

        # 检查响应状态码
        if response.status_code == 200:
            print(f"Success: {response.status_code}")
            print("Please parse the response data as needed.")
            return response.json()  # 返回解析后的JSON数据
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)

def get_image_uuid():
    return str(uuid.uuid4())

def get_save_dir():
    return '/home/pci/dong/AIGC-image'

def create_save_dir(save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

def get_image_hash(image_path):
    """生成图片的感知哈希值"""
    image = Image.open(image_path)
    hash_value = imagehash.phash(image)
    return str(hash_value)