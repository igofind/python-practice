# -*- coding: utf-8 -*-

from selenium import webdriver
import time


def main():
    chrome = webdriver.Chrome()
    chrome.get("https://free-ss.site")
    # 页面中作了定时，只能用强行等待
    # 强行等待
    time.sleep(6)
    # 隐性等待，最多等待10秒
    # chrome.implicitly_wait(10)
    page = chrome.page_source
    print(page)
    chrome.quit()


if '__main__' == __name__:
    main()
