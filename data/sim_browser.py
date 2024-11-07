from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 创建一个WebDriver实例
driver = webdriver.Chrome()  # 替换为你自己的chromedriver路径

# 打开登录页面
driver.get("https://laprompt.com/auth/login")

# 等待页面加载并查找 Turnstile 验证元素（需要在浏览器中查找 Turnstile 表单字段）
time.sleep(3)

# 查找并处理 Turnstile 验证，模拟人工点击（视具体情况而定）
turnstile_token = driver.execute_script("return window.turnstile.getToken()")

# 打印获取的 Token
print("cf_turnstile_token:", turnstile_token)

# 关闭浏览器
driver.quit()

# 然后使用获取到的 Token 填写请求数据
