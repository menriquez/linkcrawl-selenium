import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

window_default_wait = 1000
total_vids = 0
root_window_handle_index = 0
root_window_handle_stack = []

crawled_urls = []

chrome_options = Options()
chrome_options.headless = False
root = webdriver.Chrome()


def crawl(local_window_handle):

    global root_window_handle_index
    global root_window_handle_stack

    root.switch_to.window(local_window_handle)
    root_window_handle_stack.append(local_window_handle)

    # check if we have already crawled and kick out if so
    if root.current_url in crawled_urls:

        root_window_handle_stack.pop()
        return 0
    else:
        crawled_urls.append(root.current_url)

    # find all the clickable links on the new page
    links = root.find_elements_by_css_selector("a")
    print("Window " + root.title + " [ " + root.current_url + " ] FOUND LINKS: " + len(links))

    global total_vids
    vids = root.find_elements_by_css_selector("video")
    if vids:
        total_vids += vids.len

    for link in links:
        click_link = root.find_element_by_link_text(link.text)
        click_link.click()
        time.sleep(3)
        total_windows = len(root.window_handles)

        # grab the window just created and recurse it
        next_click_hnd = root.window_handles[total_windows-1]
        if crawl(next_click_hnd):
            print("Window " + root.title + " [ " + hnd + " ] SUCCESSFULLY scraped...")

        else:
            print("Window " + root.title + " [ " + hnd + " ] ALREADY PROCESSED skipping...")

        # close the current window and switch to the root one
        root.close()
        root.switch_to.window(root_window_handle_stack[-1])

    root_window_handle_stack.pop()
    return 1


root.get('https://krksol-miraclebust.com')
time.sleep(3)

#root.implicitly_wait(window_default_wait)
hnd = root.current_window_handle
print("current window handle="+hnd)
crawl(hnd)


root.quit()
