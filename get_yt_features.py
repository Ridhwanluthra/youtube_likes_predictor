import yt_page_interact as yt
from pymongo import MongoClient
from selenium import webdriver
from pymongo.errors import DuplicateKeyError
import logging

logging.basicConfig(filename='feature_extraction.log', filemode='w', level=logging.DEBUG)

client = MongoClient()
db = client.precog
dic = db.playlist.find()

browser = webdriver.PhantomJS()
# browser = webdriver.Firefox()
browser.set_window_size(1120, 567)

vid_count = 0
for i in range(dic.count()):
    logging.info(dic[i]['_id'])
    logging.info(vid_count)
    vid_count += 1
    features = yt.get_video_stats(browser, 'https://www.youtube.com/watch?v=' + dic[i]['_id'])
    # print(features)
    if features == None:
        print('skipping this one...')
        continue
    features.update({'_id': dic[i]['_id']})
    try:
        db.features.insert(features)
    except DuplicateKeyError as e:
        print(e)
    print()