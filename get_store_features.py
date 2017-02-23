from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
# from extract_data import get_all_data
from num_results import get_backlinks
import time

client = MongoClient()
db = client.precog
dic = db.complete_remove.find()
print(dic.count())
for i in range(dic.count()):
    print(i)
    if i < 494:
        continue
    num_links = get_backlinks(dic[i]['_id'])
    try:
        db.backlinks.insert({'_id': dic[i]['_id'], 'links': num_links})
    except DuplicateKeyError as e:
        print(e)
    time.sleep(1)
# dic = db.playlist.find()

# vid_count = 0
# for i in range(dic.count()):
#     vid_count += 1
#     print(vid_count)
#     # if vid_count < 4880:
#     #     continue
#     features = get_all_data(dic[i]['_id'])
#     # print(features)
#     # if features == None:
#     #     print('skipping this one...')
#     #     continue
#     features.update({'_id': dic[i]['_id']})
#     try:
#         db.api_crawl_features.insert(features)
#     except DuplicateKeyError as e:
#         print(e)