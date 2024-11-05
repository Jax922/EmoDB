# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# # 设置 Chrome 选项
# chrome_options = Options()
# chrome_options.binary_location = "/usr/bin/google-chrome"  # 显式指定 Chrome 的路径

# # 启用无头模式
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 硬件加速
# chrome_options.add_argument("--no-sandbox")  # 必须加上这个选项，避免沙箱错误
# chrome_options.add_argument("--remote-debugging-port=9222")  # 设置调试端口

# # 使用 webdriver_manager 自动下载和管理 chromedriver
# chrome_driver_path = ChromeDriverManager().install()

# # 创建 Service 对象来指定 ChromeDriver 的路径
# service = Service(chrome_driver_path)
# service.log_path = "chromedriver.log"  # 输出日志路径
# # 创建 WebDriver 实例，传递 Service 对象和 Chrome 配置
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # 打开网页
# driver.get("https://laprompt.com")

# # 等待页面加载
# time.sleep(3)

# # 执行 JavaScript 来获取 Turnstile Token
# turnstile_token = driver.execute_script("return window.turnstile.getToken()")

# # 打印获取到的 Token
# print("cf_turnstile_token:", turnstile_token)

# # 关闭浏览器
# driver.quit()


from selenium import webdriver


driver = webdriver.Chrome()
driver.get("https://www.google.com")


title = driver.title
print(title)
