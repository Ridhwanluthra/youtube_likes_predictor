from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

address = 'https://www.youtube.com/playlist?list=PLirAqAtl_h2rTbOXU2Oc-7WBBHmFrnyUC'

# browser = webdriver.Firefox()
browser = webdriver.PhantomJS()
print('phantom done')
browser.get(address)
time.sleep(4)
print('i am online')
htmlElem = browser.find_element_by_tag_name('html')
htmlElem.send_keys(Keys.END)
try:
    while 1:
        elem = browser.find_element_by_class_name('load-more-button')
        elem.click()
        time.sleep(2)
        htmlElem.send_keys(Keys.END)
except NoSuchElementException as e:
    vids = browser.find_elements_by_class_name('pl-video-title-link')
    for i in range(len(vids)):
        print(vids[i].get_attribute('href'))
finally:
    browser.quit()