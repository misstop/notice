import logging
import re
import datetime
from notice.items import SecondBaseNoticeItem
from notice.settings import BIBOX_CYCLE_TIME, CHECK_TIME_THRESHOLD
from pyquery import PyQuery as pq
import scrapy
import time
import json
import tweepy
import requests


def string2datetime(str, format="%Y-%m-%dT%H:%M:%SZ"):
    return datetime.datetime.strptime(str, format)


def utc2local(utc_date):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    res_time = string2datetime(utc_date) + offset
    print(res_time)
    return res_time


class BittrexSpider(scrapy.Spider):
    name = 'bittrex'
    mainUrl = "https://twitter.com/bittrexexchange"
    tweetName = "bittrexexchange"
    consumer_key = "8nBFxD0eidkfdT01hPC4jGN1q"
    consumer_secret = "WGLnM3ihIta0ykSqWbxya4pmbShuk9u5EYGg9pRkQcCQqnHkhh"
    access_token = "887348462806679552-sZ2oOakXIICdR3sqN3XZNytnDU7qXH6"
    access_token_secret = "NEjE1pnhiyXG4qJ9McIIvaAUPkdBjfEFV8aspjPR1H5m4"
    start_urls = ['https://twitter.com']

    def parse(self, response):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        list = api.user_timeline(screen_name=self.tweetName, count=1, tweet_mode="extended", exclude_replies="true",
                                 include_rts=1)
        jsonContent = list[0]
        jsonData = jsonContent._json
        try:
            content = jsonData['retweeted_status']['full_text']
        except:
            content = jsonData['full_text']
        title = content[0:15] + "..."
        created_at = jsonData['created_at'].replace("+0000 ", "")
        time_tuple = time.strptime(created_at, "%a %b %d %H:%M:%S %Y")
        ms = time.mktime(time_tuple) + 8 * 60 * 60
        dateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ms))
        Id = jsonData['id_str']
        url = "https://twitter.com/" + str(jsonData['user']['screen_name']) + "/status/" + str(Id)
        item = SecondBaseNoticeItem()
        item['name'] = 'bittrex'
        item['resource'] = 'bittrex.com'
        item['url'] = url
        item['title'] = title
        item['main'] = content
        item['time'] = dateTime
        logging.log(logging.INFO, '[Bittrex] Get item:', item)
        yield item