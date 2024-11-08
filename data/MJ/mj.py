from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup

# 配置 WebDriver
driver = webdriver.Chrome()

# 打开网页
driver.get("https://www.midjourney.com/explore?tab=random")  # 替换成你想爬取图片的网页

# 等待页面加载（视情况设置时间，或者使用显式等待）
time.sleep(5)

body = driver.find_element(By.TAG_NAME, 'body')

html = driver.page_source

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html, 'html.parser')

# 找到id为pageScroll的div
page_scroll = soup.find(id='pageScroll')

# 提取所有a标签
links = page_scroll.find_all('a')

# 提取a标签中的href属性
image_urls = []
for link in links:
    href = link.get('href')
    image_urls.append(href)

for url in image_urls:
    print(url)


# # 定位到图片元素（例如通过标签名、class等）
# images = driver.find_elements(By.TAG_NAME, 'img')  # 根据实际情况选择合适的定位方式

# # 下载图片
# for img in images:
#     src = img.get_attribute('src')
#     if src:
#         try:
#             img_data = requests.get(src).content
#             with open("images/" + src.split("/")[-1], 'wb') as file:
#                 file.write(img_data)
#         except Exception as e:
#             print(f"Error downloading {src}: {e}")

# # 关闭浏览器
driver.quit()
