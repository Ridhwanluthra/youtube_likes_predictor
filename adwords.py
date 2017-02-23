from pymongo import MongoClient
import pandas as pd
import csv
from collections import deque

def create_csv_for_planner():
    client = MongoClient()
    db = client.precog

    dic = db.complete_remove.find()

    df = pd.DataFrame(list(dic))

    tags = deque()
    for i in range(len(df['tags'])):
        tags.extend(df['tags'][i])

    num = 0
    for i in range(len(tags)):
        if i % 700 == 0:
            num += 1
        name = 'tags' + str(num) + '.csv'
        with open(name, 'a', newline='') as csvfile:
            cw = csv.writer(csvfile)
            cw.writerow([tags[i]])

def extract_data_from_adwords_csv():
    # i need 1, 3, 4, 5
    data = pd.DataFrame()
    for i in range(1,18):
        file = './adwords_results/' + str(i) + '.csv'
        csvfile = pd.read_csv(file, encoding='utf-16')
        csvfile.columns = ['all']
        data = data.append(csvfile, ignore_index=True)
    # print(data)
    tags = deque()
    searches = deque()
    bid = deque()
    competition = deque()
    for i in range(len(data['all'])):
        li = data['all'][i].split('\t')
        for j in [1, 3, 4, 5]:
            if li[j] == '':
                li[j] = 0

            if j == 1:
                tags.append(li[j].casefold())

            elif j == 3:
                searches.append(li[j])

            elif j == 4:
                competition.append(float(li[j]))

            elif j == 5:
                bid.append(float(li[j]))

    df = pd.DataFrame()
    df['tags'] = tags
    df['searches'] = searches
    df['bid'] = bid
    df['competition'] = competition
    df = df[df['searches'] != 0]
    # print(df)
    searches = df['searches'].values
    for i in range(len(searches)):
        searches[i] = int(searches[i].split()[0].replace('K', '000').replace('M', '000000'))
    df['searches'] = df['searches'].astype(int)
    df = df[df['searches'] != 0]
    df = df.drop_duplicates('tags').reset_index(drop=True)
    return df