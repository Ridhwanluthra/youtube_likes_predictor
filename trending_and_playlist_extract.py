from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

client = MongoClient()
db = client.precog

def trending_videos():
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
        db.youtube_urls.insert({'url': vid.get_attribute('href'), 'country': 'India'})


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
            db.youtube_urls.insert({'url': vid.get_attribute('href'), 'country': name_list[i]})
            # time.sleep(2)
            # for j in range(len(vids)):
            #     print(vids[j].get_attribute('href'))
    # except Exception as e:
    #     print(e)
    # finally:
        # pass
    browser.quit()

def playlist_videos(address):
    # browser = webdriver.Firefox()
    # browser = webdriver.PhantomJS()
    # print('phantom done')
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
        vids = browser.find_elements_by_class_name('pl-video')
        urls = []
        for i in range(len(vids)):
            if vids[i].get_attribute('data-video-id') == 'IKxc40rFl6Y':
                continue
            urls.append({'_id' : vids[i].get_attribute('data-video-id')})
        return urls
    finally:
        pass
        # browser.quit()

if __name__ == '__main__':
    # address = 'https://www.youtube.com/user/MyTop10Videos/playlists?flow=grid&view=50&shelf_id=4'
    # browser = webdriver.PhantomJS()
    browser = webdriver.Firefox()
    print('phantom done')
    # browser.get(address)
    time.sleep(4)
    print('i am online')
    playlists_link = browser.find_elements_by_class_name('yt-uix-tile-link')
    # took 2 specific links; will remove this for a page of playlists
    pl_list = ['https://www.youtube.com/playlist?list=PLWwAypAcFRgKFlxtLbn_u14zddtDJj3mk', 'https://www.youtube.com/playlist?list=PLPZgiga_0D3HWboabRTgRn5032sbL395g']
    # uncomment this for taking from page of playlist; doing this because webelem becomes stale
    # for i in range(len(playlists_link)):
    #     pl_list.append(playlists_link[i].get_attribute('href'))

    from pymongo.errors import BulkWriteError
    for i in range(len(pl_list)):
        try:
            db.playlist.insert_many(playlist_videos(pl_list[i]), ordered = False)
        except BulkWriteError as e:
            pass
        finally:
            print(db.playlist.count())

# TODO: organise the content properly