---
layout: post
title: 自动化下载群晖共享的文件
date: 2023-11-07 23:28+0800
description: 
tags: automation
giscus_comments: true
categories: icenv
---

接到需求，需要从合作伙伴提供的群晖NAS上，批量下载大量文件。手动下载太费事费时，没有价值；并且PC的带宽有限，只能将批量串行下载，手动的话中间容易出现空闲，导致总的下载时长很长。

因此写了脚本做自动化下载，如下：

```python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def is_download_completed(directory):
    """
    Check if all files in the specified directory have finished downloading.
    """
    for filename in os.listdir(directory):
        # 下载过程中，临时文件的名字是.crdownload，因此这里判断是否有这样的文件
        if filename.endswith('.crdownload') or filename.endswith('.part'):
            return False
    return True

def download(link, pw):
    # 设置Chrome选项以静默模式运行（无界面模式）
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # 设置下载文件的默认目录到 F:\Downloads
    prefs = {
        "download.default_directory": r"F:\Downloads",  # 使用原始字符串来避免转义
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # 初始化WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 打开登录页面
    driver.get(link)

    # 填写登录信息并提交表单
    wait = WebDriverWait(driver, 10)
    password_field = wait.until(EC.element_to_be_clickable((By.ID, "login_passwd")))
    password_field.send_keys(pw)
    driver.find_element(By.ID, "ext-gen62").click()

    # 等待页面加载
    time.sleep(5)

    # 定位到下载链接并点击
    download_link = driver.find_element(By.ID, "ext-gen71")
    download_link.click()

    # 等待文件下载完成
    while not is_download_completed(download_path):
        time.sleep(1)  # 每隔1秒检查一次

    # 关闭浏览器
    driver.quit()


if __name__ == "__main__":
    # 指定Excel文件的路径
    file_path = "F:\\Downloads\\files2download_from_Synology.xlsx"
    df = pd.read_excel(file_path, usecols=['链接', '密码'], engine='openpyxl')

    for _, row in df.iterrows():
        link, pw = *row
        print(f"Downloading {link} with password {pw}")
        download(link, pw)
```

运行，开始下载：
![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/9669aa6c-87fd-4fa3-a908-97a0bbce4570)
