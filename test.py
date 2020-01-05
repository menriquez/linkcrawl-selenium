import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

window_default_wait = 1000
total_vids = 0

crawled_urls = []

chrome_options = Options()
chrome_options.headless = True
root = webdriver.Chrome(chrome_options=chrome_options)


def crawl(local_window_handle):

    root.switch_to.window(local_window_handle)
    # check if we have already crawled and kick out if so
    if root.current_url in crawled_urls:
        root.close()
        return 0
    else:
        crawled_urls.append(root.current_url)

    # find all the clickable links on the new page
    links = root.find_elements_by_css_selector("a")

    global total_vids
    total_vids += root.find_elements_by_css_selector("video").count()

    for link in links:
        click_link = root.find_element_by_link_text(link.text)
        click_link.click()
        cur_click_hnd = root.window_handles[0]
        next_click_hnd = root.window_handles[1]
        if crawl(next_click_hnd):
            print("Window " + root.title + " [ " + hnd + " ] SUCCESSFULLY scraped...")
            root.close()
        else:
            print("Window " + root.title + " [ " + hnd + " ] ALREADY PROCESSED skipping...")

    return 1


root.get('https://krksol-miraclebust.com')

#root.implicitly_wait(window_default_wait)
hnd = root.current_window_handle
print("current window handle="+hnd)
crawl(hnd)


root.quit()
