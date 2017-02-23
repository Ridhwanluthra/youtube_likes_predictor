from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, datetime
from pymongo import MongoClient
import signal

# TODO: proper handling of exceptions

def handler(signo, frame):
    raise TimeoutError

signal.signal(signal.SIGALRM, handler)

categories = ['Autos and Vehicles','Comedy','Education','Film & Animation','Gaming','Howto & Style','Music','News & Politics','Nonprofits & Activism','People & Blogs','Pets & Animals','Science & Technology','Sports','Travel & Events']

def get_time_watched(dur):
    dur = dur.split()
    dur[0] = int (dur[0].replace(',',''))
    if (dur[1] == "years"):
        dur[0] = dur[0] * 365 * 24 * 60 * 60
    elif (dur[1] == "days"):
        dur[0] = dur[0] * 24 * 60 * 60
    elif (dur[1] == "hours"):
        dur[0] = dur[0] * 60 * 60
    elif (dur[1] == "minutes"):
        dur[0] = dur[0] * 60
    return dur[0]

def get_video_length(length):
    length = length.split(':')
    mul = 1
    int_len = 0
    for i in range(len(length) - 1, -1, -1):
        int_len += mul * int(length[i])
        mul *= 60
    return int_len

def time_from_publish(date):
    date = ' '.join(date.split()[2:]).replace(',', '')
    # if "hour" in date:
    #     date = date.split(' ')
    #     return int(date[0]) * 60 * 60
    # if "day" in date:
    #     date = date.split(' ')
    #     return int(date[0]) * 24 * 60 * 60
    p_date = datetime.datetime.strptime(date, "%b %d %Y")
    c_date = datetime.datetime.now()
    elapsed = (c_date - p_date).days * 24 * 60 * 60
    return elapsed

def get_video_stats(browser, address):
    # browser = webdriver.Firefox()
    
    # browser.implicitly_wait(10)
    browser.get(address)
    # print('online')
    # browser.set_page_load_timeout(5)
    # time.sleep(4)
    # while browser.find_element_by_tag_name('html') == None:
    #     pass
    htmlElem = browser.find_element_by_tag_name('html')
    try:
        signal.alarm(5)
        while htmlElem == None:
            htmlElem = browser.find_element_by_tag_name('html')
        signal.alarm(0)
    except TimeoutError:
        print('timeout in loading....')

    # htmlElem.send_keys(Keys.END)
    htmlElem.send_keys(Keys.PAGE_DOWN)
    # time.sleep(4)
    htmlElem.send_keys(Keys.PAGE_UP)
    final_dict = dict()
    # click on more button
    try:
        elem = browser.find_element_by_id('action-panel-overflow-button')
        elem.click()
    except:
        return
    # time.sleep(2)
    try:
        # click on statistics button
        elem = browser.find_element_by_class_name('action-panel-trigger-stats')
        signal.alarm(3)
        while elem == None:
            print(1)
            elem = browser.find_element_by_class_name('action-panel-trigger-stats')
        signal.alarm(0)
        elem.click()
        # time.sleep(4)

        # get views info
        try:
            elem = browser.find_element_by_class_name('stats-bragbar-views')
            signal.alarm(3)
            while elem == None:
                elem = browser.find_element_by_class_name('stats-bragbar-views')
            signal.alarm(0)
            final_dict['views'] = int(elem.text.split('\n')[1].replace(',', ''))
        except:
            print('timeout in views.....')
            final_dict['views'] = None

        # get watch-time
        # busy waiting not needed due same page as views
        try:
            elem = browser.find_element_by_class_name('stats-bragbar-watch-time')
            final_dict['watch_time'] = get_time_watched(elem.text.split('\n')[1])
        except:
            final_dict['watch_time'] = None

        # get subscribtions driven
        try:
            elem = browser.find_element_by_class_name('stats-bragbar-subscribers')
            final_dict['subscribtions_driven'] = int(elem.text.split('\n')[1].replace(',', ''))
        except:
            final_dict['subscribtions_driven'] = None

        # get shares
        try:
            elem = browser.find_element_by_class_name('stats-bragbar-shares')
            final_dict['shares'] = int(elem.text.split('\n')[1].replace(',', ''))
        except:
            final_dict['shares'] = None
    except:
        print('timeout in stats....')
        final_dict['shares'] = None
        final_dict['subscribtions_driven'] = None
        final_dict['watch_time'] = None
        final_dict['views'] = None

    # get number of subscribers of channel
    # busy waiting not needed as its there or not
    try:
        elem = browser.find_element_by_class_name('yt-subscriber-count')
        final_dict['subscribers'] = int(elem.text.replace(',', ''))
    except:
        final_dict['subscribers'] = None
    
    # get number of likes
    try:
        elem = browser.find_element_by_class_name('like-button-renderer-like-button')
        elem = elem.find_element_by_class_name('yt-uix-button-content')
        final_dict['likes'] = int(elem.text.replace(',', ''))
    except:
        final_dict['likes'] = None
    
    # get number of dislikes
    try:
        elem = browser.find_element_by_class_name('like-button-renderer-dislike-button')
        elem = elem.find_element_by_class_name('yt-uix-button-content')
        final_dict['dislikes'] = int(elem.text.replace(',', ''))
    except:
        final_dict['dislikes'] = None

    # get published on
    try:
        elem = browser.find_element_by_class_name('watch-time-text')
        final_dict['publish_time'] = time_from_publish(elem.text)
    except:
        final_dict['publish_time'] = None

    # get number of comments
    try:
        htmlElem.send_keys(Keys.PAGE_DOWN)
        elem = browser.find_element_by_class_name('comment-section-header-renderer')
        signal.alarm(3)
        while elem == None:
            elem = browser.find_element_by_class_name('comment-section-header-renderer')
        signal.alarm(0)
        final_dict['comments'] = int(elem.text.split(' ')[2].replace(',', ''))
    except:
        final_dict['comments'] = None
    
    # get length of video
    try:
        elem = browser.find_element_by_class_name('ytp-play-button')
        elem.click()
        signal.alarm(2)
        elem = browser.find_element_by_class_name('ytp-time-duration')
        while elem == None:
            elem = browser.find_element_by_class_name('ytp-time-duration')
        signal.alarm(0)
        final_dict['video_length'] = get_video_length(elem.text)
    except:
        final_dict['video_length'] = None

    # subs exist or not
    try:
        elem = browser.find_element_by_class_name('ytp-subtitles-button')
        final_dict['subs_exist'] = elem.is_displayed()
    except:
        final_dict['subs_exist'] = None
    
    # get type of video
    try:
        elem = browser.find_elements_by_class_name('watch-info-tag-list')
        signal.alarm(2)
        while elem == None:
            elem = browser.find_elements_by_class_name('watch-info-tag-list')
        signal.alarm(0)
        final_dict['video_category'] = categories.index(elem[0].get_attribute('innerText').replace('\n', '').replace(' ', ''))
    except:
        final_dict['video_category'] = None

    # printing all data
    # print('watch_time', final_dict['watch_time'])
    # print('views: ', final_dict['views'])
    # print('subscribtions_driven', final_dict['subscribtions_driven'])
    # print('shares', final_dict['shares'])
    # print('subscribers: ', final_dict['subscribers'])
    # print('likes', final_dict['likes'])
    # print('dislikes', final_dict['dislikes'])
    # print('publish_time', final_dict['publish_time'])
    # print('comments', final_dict['comments'])
    # print('video_length', final_dict['video_length'])
    # print('subs_exist', final_dict['subs_exist'])
    # print('video_category', final_dict['video_category'])
    
    return final_dict
    # return dict(views, **watch_time, **subscribtions_driven, **shares, **subscribers, **likes, **dislikes, **publish_time, **comments, **video_length, **subs_exist, **video_category)

    # TODO: quality of video

if __name__ == '__main__':
    client = MongoClient()
    db = client.precog
    dic = db.playlist.find()
    
    # browser = webdriver.PhantomJS()
    print('phantom_done')
    browser = webdriver.Firefox()
    # browser.set_window_size(1120, 567)
    print('window set')
    print(dic.count())
    for i in range(dic.count()):
        print(dic[i]['_id'])
        get_video_stats(browser, 'https://www.youtube.com/watch?v=' + dic[i]['_id'])
        print()