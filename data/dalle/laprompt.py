import sys
import os

from tqdm import tqdm
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils as UTILS
import db as DB




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
        print(f"Image successfully downloaded: {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


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

n = 0
total_imgs = 0

print("Start to download images from laprompt.com")
while n<2:
    response = UTILS.send_request(next_url, headers=default_headers)
    all_results = response['results']
    next_url = response['next']
    print(f"Total imgs in this step: {len(response['results'])}")
    n += 1

    print(f"Total imgs: {len(all_results)}")

    imgDB = DB.MongoDBHandler()

    for res in tqdm(all_results):
        image_counts = len(res['images'])
        image_url = res['images'][image_counts-1]["image"]
        image_type = image_url.split('.')[-1]
        image_name = UTILS.get_image_uuid() + '.' + image_type
        image_path = os.path.join(save_dir+"/"+image_name)
        print(f"Downloading image: {image_path}")
        download_image(image_url, image_path)
        print(f"Downloaded image: {image_path}")
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
    imgDB.close()
    total_imgs += len(all_results)


print(f"Total imgs: {len(all_results)}")
print("Have done the job!")



