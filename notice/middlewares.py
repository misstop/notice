# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
from scrapy import signals
import scrapy
from notice.spiders.binance import BinanceSpider
import requests
import random

# auth_tokens = [
#     {
#         'consumer': {
#             'consumer_key': '3LT1QDxdbzF1lXgzWTMIZ4Xw0',
#             'consumer_secret': 'hHCieQP7yUFERI9XSxRotA25uXKE2Hw1lWCe2DLgXjRYSn3h9z'
#             },
#         'access': {
#             'access_token': '882868123711307776-3CsSiWq1H461ezSdGl1l05wGEW78hCy',
#             'access_token_secret': 'Lisxqgz0BIwrUtt3vqtnS0WUi8eyMv18gTyoLr9a6BSBg'
#             }
#     },
#     {
#         'consumer': {
#             'consumer_key': 'UafXxpzgGISEqbx0Axgq1lj0X',
#             'consumer_secret': 'vE3TuZpPlcQz1VsDZaibxspHIHoJNrJd0kwwUcxSlTY2NfWzIv'
#             },
#         'access': {
#             'access_token': '882868123711307776-sQmqCPl1q4g3mwccvpEZLeSkdeZVyeW',
#             'access_token_secret': 'ikeQZejSxrj1fRzhrdIdjXiSqoCLfSTk00mZOBiqfMJih'
#             }
#     },
#     {
#         'consumer': {
#             'consumer_key': 'gSHX2OsuVgtmhSruVsbLmjof0',
#             'consumer_secret': '2gsGG9z3NPKgYOTH8RE5KzGreLWTTYPiga0V0MzCd2Ma7N86Os'
#             },
#         'access': {
#             'access_token': '882868123711307776-Haj2zgsvoPnpevDjylEfdzeAMvHYJ1l',
#             'access_token_secret': 'BJgJ9VydFXvqtPO4kKokNYBH0h2Xq5QTwQD2Nqb3OCskc'
#             }
#     }
# ]


# class BinanceDownloadMiddleware():
#     def process_request(self, request, spider):
#         if isinstance(spider, BinanceSpider):
#             print('使用币安中间件')
#             response = requests.post(request.url)
#             return scrapy.http.Response(url=request.url, body=response.text.encode('utf8'))

        # if isinstance(spider, TwitterSpider):
        #     token = random.choice(auth_tokens)
        #     auth = tweepy.OAuthHandler(token['consumer']['consumer_key'], token['consumer']['consumer_secret'])
        #     auth.set_access_token(token['access']['access_token'], token['access']['access_token_secret'])
        #     api = tweepy.API(auth)
        #
        #     screen_name = request.meta['screen_name']
        #     result = list(api.user_timeline(id=screen_name, count=TWEEN_COUNT))[0]
        #     result = result._json
        #     resp = {}
        #     resp['screen_name'] = result.author.screen_name
        #     resp['time'] = str(result.created_at)
        #     resp['text'] = str(result.text)
        #     body_str = json.dumps(resp).encode('utf8')
        #     return scrapy.http.Response(url=request.url, body=body_str)


class NoticeSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class NoticeDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
