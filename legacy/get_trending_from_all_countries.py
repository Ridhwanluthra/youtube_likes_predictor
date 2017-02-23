from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from yt_page_interact import get_video_stats

address = 'https://www.youtube.com/feed/trending?gl=IN'

browser = webdriver.Firefox()
# browser = webdriver.PhantomJS()
print('phantom done')
browser.get(address)
time.sleep(4)
print('i am online')
htmlElem = browser.find_element_by_tag_name('html')
htmlElem.send_keys(Keys.END)
vids = browser.find_elements_by_class_name('yt-lockup-title')
time.sleep(1)
for j in range(len(vids)):
    vid = vids[j].find_element_by_tag_name('a')
    print(vid.get_attribute('href'))
print('india done')
# try:
elem = browser.find_element_by_id('yt-picker-country-button')
elem.click()
time.sleep(2)
htmlElem.send_keys(Keys.END)
elem = browser.find_elements_by_class_name('yt-picker-item')
time.sleep(5)
elem_list = []
name_list = []
for i in range(len(elem)):
    # name = browser.find_elements_by_class_name('yt-picker-region-name')
    # print(elem[i].tag_name)
    if elem[i].tag_name != 'a':
        continue
    elem_list.append(elem[i].get_attribute('href'))
    name_list.append(elem[i].find_element_by_class_name('yt-picker-region-name').get_attribute('innerText'))
print(elem_list)
print(name_list)
for i in range(len(elem_list)):
    # brow = webdriver.Firefox()
    browser.get(elem_list[i])
    time.sleep(5)
    vids = browser.find_elements_by_class_name('yt-lockup-title')
    time.sleep(1)
    for j in range(len(vids)):
        vid = vids[j].find_element_by_tag_name('a')
        print(vid.get_attribute('href'))
        # time.sleep(2)
        # for j in range(len(vids)):
        #     print(vids[j].get_attribute('href'))
# except Exception as e:
#     print(e)
# finally:
    # pass
browser.quit()