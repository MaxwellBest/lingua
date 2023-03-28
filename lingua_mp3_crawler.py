from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re 

article = "London"
accent = "American"

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=D:\\ChromePortable64\\Data\\profile")
options.add_argument('profile-directory=Profile 1')
driver = webdriver.Chrome(executable_path=r'"D:\chromedriver_win32\chromedriver.exe"', chrome_options=options)


# driver.get("https://www.google.com.tw")

# 打开登录页面
driver.get("https://lingua.com/login/google/")

# 跳转到阅读页面
driver.get(f"https://lingua.com/english/reading/{article}/")

# # 等待元素出现
# wait.until(EC.presence_of_element_located((By.CLASS_NAME, "wrapper-lingua-speakers")))

# 等待元素出现
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "wrapper-lingua-speakers")))

# 获取解析后的HTML内容
html = driver.execute_script("return document.documentElement.outerHTML")

# # 获取页面源码
# html = driver.page_source

# 解析页面源码
soup = BeautifulSoup(html, "html.parser")

# 获取所有的 data-filename 属性
# data_filenames = [elem['data-filename'] for elem in soup.select('[data-filename]')]
# 找到 class 属性为 "speaker-box"，并且包含 "American English" 文本的 div 元素
american_div = soup.select_one(f'.speaker-box:contains("{accent} English")')
# 获取其 data-filename 属性
data_filenames = american_div['data-filename']
url_prefix = "https://lingua.com/"
filepath_prefix = "D:/lingua/"

if type(data_filenames) == list:
    for f in data_filenames:
        url,filename = url_prefix + f.replace("../../../", ""), filepath_prefix + f.replace("../../../", "")
        filename = filename.replace(re.search(r'english-\w+-(.*).mp3', filename).group(1),accent)
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
else:
    url,filename = url_prefix + data_filenames.replace("../../../", ""), filepath_prefix + data_filenames.replace("../../../", "")
    filename = filename.replace(re.search(r'english-\w+-(.*).mp3', filename).group(1),accent)
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
        
# 关闭浏览器
driver.quit()
