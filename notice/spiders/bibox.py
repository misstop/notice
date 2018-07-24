import logging
import re
import datetime
from notice.items import SecondBaseNoticeItem
from notice.settings import BIBOX_CYCLE_TIME, CHECK_TIME_THRESHOLD
from pyquery import PyQuery as pq
import scrapy
import time
import json
import requests

def string2datetime(str,format="%Y-%m-%dT%H:%M:%SZ"):
    return datetime.datetime.strptime(str,format)
def utc2local(utc_date):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    res_time = string2datetime(utc_date) + offset
    print(res_time)
    return res_time

class BiboxSpider(scrapy.Spider):
    name = 'bibox.com'
    base_url="https://bibox.zendesk.com"
    notice_url = 'https://bibox.zendesk.com/hc/api/internal/recent_activities?locale=zh-cn&page=1&per_page=1&locale=zh-cn'

    def start_requests(self, ):
        # while True:
            yield scrapy.Request(url=self.notice_url,
                    dont_filter=True,
                    callback=self.parse_item)
            # time.sleep(BIBOX_CYCLE_TIME)
            # time.sleep(1)

    def parse_item(self, response):
        response_json = json.loads(response.body.decode('utf8'))
        if not response_json['activities']:
            return
        notice = response_json['activities'][0]

        item = SecondBaseNoticeItem()
        item['name'] = 'Bibox'
        item['resource'] = 'bibox.com'

        item['url'] = self.base_url+notice['url']

        doc_detail=pq(requests.get(item['url']).text)
        item['title'] = doc_detail('.article-header h1').text()
        item['main'] =doc_detail('.article-body').text()

        date = doc_detail('.meta-data time').attr('datetime')

        item['time'] = utc2local(date).strftime("%Y-%m-%d %H:%M:%S")

        logging.log(logging.DEBUG, '[BITFINE] Get item:', item)
        yield item

