from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import sys
sys.path.append('./YTCrawl')
from crawler import Crawler
import datetime

DEVELOPER_KEY = "AIzaSyAiQmQGC0AmwosgZ9Yz2yCSyUlQrnnIixc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

def data_from_api(video_id):
    # video_ids = 'LZ34LlaIk88'

    # channel_ids = 'UCANLZYMidaCbLQFWXBC95Jg'

    # can be taken: contentDetails
    data = dict()
    caption = youtube.captions().list(videoId=video_id, part='snippet').execute()
    print(caption['items'][0]['snippet']['language'])
    video_response = youtube.videos().list(id=video_id, part='statistics, snippet, topicDetails').execute()
    try:
        vid = video_response.get('items', [])[0]
    except Exception as e:
        print(e)
        return dict()
    try:
        data['comment_count'] = vid['statistics']['commentCount']
    except Exception as e:
        data['comment_count'] = 0
        print(e)

    try:
        data['view_count'] = vid['statistics']['viewCount']
    except Exception as e:
        data['view_count']
        print(e)

    try:
        data['favorite_count'] = vid['statistics']['favoriteCount']
    except Exception as e:
        data['favorite_count'] = 0
        print(e)

    try:
        data['dislike_count'] = vid['statistics']['dislikeCount']
    except Exception as e:
        data['dislike_count'] = 0
        print(e)
    
    try:
        data['likes_count'] = vid['statistics']['likeCount']
    except Exception as e:
        data['likes_count'] = 0
        print(e)

    data['channel_id'] = vid['snippet']['channelId']

    try:
        data['category_id'] = vid['snippet']['categoryId']
    except Exception as e:
        data['category_id'] = 0
        print(e)

    try:
        data['tags'] = vid['snippet']['tags']
    except Exception as e:
        data['tags'] = []
        print(e)

    channel_id = vid['snippet']['channelId']
    channel_response = youtube.channels().list(id=channel_id, part='statistics, snippet, brandingSettings').execute()
    try:
        chan = channel_response['items'][0]
    except Exception as e:
        print(e)
        return data
    # print(chan)
    try:
        data['channel_publish'] = chan['snippet']['publishedAt']
    except Exception as e:
        print(e)
        data['channel_publish'] = ''
    try:
        data['featured_channels'] = chan['brandingSettings']['channel']['featuredChannelsUrls']
    except Exception as e:
        data['featured_channels'] = []
        print(e)

    try:
        data['channel_keywords'] = chan['brandingSettings']['channel']['keywords']
    except Exception as e:
        data['channel_keywords'] = ''
        print(e)

    try:
        data['channel_comment_count'] = chan['statistics']['commentCount']
    except Exception as e:
        data['channel_comment_count'] = 0
        print(e)

    try:
        data['channel_view_count'] = chan['statistics']['viewCount']
    except Exception as e:
        data['channel_view_count'] = 0
        print(e)

    try:
        data['channel_video_count'] = chan['statistics']['videoCount']
    except Exception as e:
        data['channel_video_count'] = 0
        print(e)

    try:
        data['channel_subscribers'] = chan['statistics']['subscriberCount']
    except Exception as e:
        data['channel_subscribers'] = 0
        print(e)

    return data

def yt_crawler(video_id):
    craw = Crawler()
    try:
        crawl_response = craw.single_crawl(video_id)
    except Exception as e:
        print(e)
        return dict()
    data = dict()
    data['shares'] = crawl_response['numShare']
    data['subscribers'] = crawl_response['numSubscriber']
    data['watch_time'] = crawl_response['watchTime']
    data['upload_data'] = (datetime.date.today() - crawl_response['uploadDate']).days * 24 * 60 * 60
    # print(data['upload_data'])
    data['daily_views'] = crawl_response['dailyViewcount']
    # print(len(data))
    return data

def get_all_data(id):
    data = data_from_api(id)
    data.update(yt_crawler(id))
    return data

# print(get_all_data('hRVfCplkKq4'))
# video_ids = 'hRVfCplkKq4'
# data_from_api(video_ids)