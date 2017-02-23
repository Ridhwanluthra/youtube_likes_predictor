from pymongo import MongoClient
from collections import deque, OrderedDict
from sklearn.neural_network import MLPRegressor
from sklearn import metrics
from new_data_test import time_from_publish
from ml_tests import train_models

def separate_likes(dic):
    likes = deque()
    for i in range(dic.count()):
        likes.append(int(dic[i]['likes_count']))
    return likes
    # db.likes.insert({'likes': list(likes)})

def process_and_fill(dic):
    # subscribers, shares, watch_time
    subscribers = deque()
    shares = deque()
    watch_time = deque()
    X = deque()
    for i in range(dic.count()):
        x = []
        for key in dic[i]:
            if key == 'likes' or key == 'channel_id' or key == '_id' or key == 'shares' or key == 'subscribers' or key == 'watch_time' or key == 'channel_keywords' or key == 'featured_channels' or key == 'tags':
                continue
            # x.append()
        
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    nn = MLPRegressor(hidden_layer_sizes=(100,100,), activation='relu')
    y_nn = nn.fit(X, y).predict(X)
    
def dict_to_list(dic):
    li = ['channel_view_count', 'channel_publish', 'category_id', 'dislike_count', 'channel_keywords', 'subscribers', 'channel_comment_count', 'view_count', 'channel_subscribers', 'channel_video_count', 'comment_count', 'favorite_count', 'shares', 'daily_views', 'watch_time', 'upload_data']
    li.sort()
    X = []
    for i in range(dic.count()):
        x = []
        for j in range(len(li)):
            if li[j] == 'shares' or li[j] == 'subscribers' or li[j] == 'watch_time' or li[j] == 'channel_keywords' or li[j] == 'tags' or li[j] == 'daily_views':
                continue
            try:
                if li[j] == 'channel_publish':
                    x.append(int(time_from_publish(dic[i][li[j]])))
                else:
                    x.append(int(dic[i][li[j]]))
            except KeyError as e:
                print(li[j])
        # assert len(x) == 11
        X.append(x)
    return X


if __name__ == '__main__':
    
    client = MongoClient()
    db = client.precog

    dic = db.complete_remove.find()

    # working_with_dicts(dic)
    
    X = dict_to_list(dic)
    y = list(separate_likes(dic))

    train_models(X,y)