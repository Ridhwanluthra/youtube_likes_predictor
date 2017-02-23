from pymongo import MongoClient
import pandas as pd
import numpy as np
import datetime


def find_none_count(dic):
    none_count = {}
    for i in range(4000):
        print(len(dic[i]))
        if len(dic[i]) == 19:
            for key in dic[i]:
                none_count[key] = 0
            break
    print('out')
    for i in range(dic.count()):
        for key in dic[i]:
            if dic[i][key] == 0 or dic[i][key] == [] or dic[i][key] == '' or dic[i][key] == None:
                none_count[key] += 1
        print(i)
    return none_count

def time_from_publish(date):
    date = date.split('T')[0].split('-')
    p_date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    c_date = datetime.date.today()
    elapsed = (c_date - p_date).days
    return elapsed

# data['shares'] = crawl_response['numShare']
#     data['subscribers'] = crawl_response['numSubscriber']
#     data['watch_time'] = crawl_response['watchTime']
#     data['upload_data'] = (datetime.date.today() - crawl_response['uploadDate']).days * 24 * 60 * 60
#     # print(data['upload_data'])
#     data['daily_views'] = crawl_response['dailyViewcount']

def process_crawler_data(dic):
    upload_data = dic['upload_data']

    shares_total = 0
    shares_av = 0
    subscribers_total = 0
    subscribers_av = 0
    watch_time_total = 0
    watch_time_av = 0
    views_total = 0
    views_av = 0

    for i in range(len(dic['shares'])):
        shares_total += dic['shares'][i]
    shares_av = shares_total / len(dic['shares'])

    for i in range(len(dic['subscribers'])):
        subscribers_total += dic['subscribers'][i]
    subscribers_av = subscribers_total / len(dic['subscribers'])

    for i in range(len(dic['watch_time'])):
        watch_time_total += dic['watch_time'][i]
    watch_time_av = watch_time_total / len(dic['watch_time'])

    for i in range(len(dic['daily_views'])):
        views_total += dic['daily_views'][i]
    views_av = views_total / len(dic['daily_views'])


def preprocess_data(dic):
    pass

# channel keywords are string separated by ' '
# featured channels is a list of channelids
# tags are a list of tags
if __name__ == '__main__':

    client = MongoClient()
    db = client.precog

    # dic = db.api_crawl_features.find()
    dic = db.complete_remove.find()

    # for key in dic[5]:
    #     print(key)

    # print(dic[5]['upload_data'])
    print(find_none_count(dic))

    # db.none_count.insert(find_none_count(dic))