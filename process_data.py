from pymongo import MongoClient
import pandas as pd
import numpy as np
import datetime
import pylab as p
from adwords import extract_data_from_adwords_csv
from collections import deque

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
    return int(elapsed)

def process_tags(tags):
    tags = pd.DataFrame(tags)
    df = extract_data_from_adwords_csv()
    searches_list = deque()
    bid_list = deque()
    competition_list = deque()
    for i in range(len(tags)):
        searches = 0
        bid = 0
        competition = 0
        for j in tags['tags'][i]:
            # gets a df with searches, bid, competition where tags are the ones we want
            result = df[df['tags'] == j.casefold()][['searches', 'bid', 'competition']].reset_index(drop=True)
            if result.empty:
                continue
            searches += result['searches'][0]
            bid += result['bid'][0]
            competition += result['competition'][0]
        # taking average of tags
        searches /= len(tags['tags'][i])
        bid /= len(tags['tags'][i])
        competition /= len(tags['tags'][i])

        searches_list.append(searches)
        bid_list.append(bid)
        competition_list.append(competition)
    tags['searches'] = searches_list
    tags['bid'] = bid_list
    tags['competition'] = competition_list
    return tags

def preprocess_data(dic):
    # a pymongo curser is passed into the function which is converted to pandas dataframe
    df = pd.DataFrame(list(dic))

    for i in df.columns:
        # channel_publish is a string the time from publish function converts it into int
        # which denotes days from publishing
        if i == 'channel_publish':
            temp = list(df[i])
            for j in range(len(temp)):
                temp[j] = time_from_publish(temp[j])
            df[i] = temp
        try:
            # converting whatever is possible into int
            df[i] = df[i].astype(float)
        except Exception as e:
            print(e)
            try:
                # we have time series data for watch_time, shares, subcribtions_driven and views
                # calculating the varience, sum of gradient and sum to input as features 
                var = []
                grad = []
                tot = []
                for j in range(len(df)):
                    var.append(np.var(df[i][j]))
                    grad.append(np.gradient(df[i][j]).sum())
                    tot.append(np.sum(df[i][j]))
                df[i + '_var'] = var
                df[i + '_grad'] = grad
                df[i + '_tot'] = tot
            except Exception as ex:
                print(ex)
    # tags = process_tags(df['tags'])
    # df['searches'] = tags['searches']
    # df['bid'] = tags['bid']
    # df['competition'] = tags['competition']
    # dropping all the values which are not needed
    df = df.drop(['daily_views', '_id', 'channel_id', 'featured_channels', 'shares', 'subscribers', 'tags', 'watch_time', 'view_count'], axis=1)
    return df
    # train_set = df.drop(['daily_views', '_id', 'channel_id', 'featured_channels', 'shares', 'subscribers', 'tags', 'watch_time', 'likes_count'], axis=1).values
    # likes = df['likes_count'].values
    # return train_set, likes

# channel keywords are string separated by ' '
# featured channels is a list of channelids
# tags are a list of tags
if __name__ == '__main__':

    client = MongoClient()
    db = client.precog

    # dic = db.api_crawl_features.find()
    dic = db.complete_remove.find()
    X, y = preprocess_data(dic)
    print(len(X), len(y))
