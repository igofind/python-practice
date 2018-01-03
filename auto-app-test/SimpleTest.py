# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def main():
    url = "https://free-ss.site/ss.json"
    chrome = webdriver.Chrome()
    chrome.get(url)
    # 强行等待
    # time.sleep(6)
    # 隐性等待，最多等待10秒
    # chrome.implicitly_wait(10)

    try:
        # 页面跳转后 title为空
        WebDriverWait(chrome, 10).until(EC.title_is(""))
        page = chrome.page_source
        print(page)
    finally:
        chrome.quit()


if '__main__' == __name__:
    main()
