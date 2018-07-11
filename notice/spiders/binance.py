import scrapy
import requests
import json
import time
from pyquery import PyQuery as pq
from notice.settings import BINANCE_CYCLE_TIME, CHECK_TIME_THRESHOLD
from notice.items import SecondBaseNoticeItem
import datetime

def string2datetime(str,format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strptime(str,format)
def utc2local(utc_date):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    res_time = string2datetime(utc_date) + offset
    print(res_time)
    return res_time


class BinanceSpider(scrapy.Spider):
    name = 'binance.com'
    notice_url = 'https://www.binance.com/public/getNotice.html?page=1&rows=1'

    def start_requests(self,):
        yield scrapy.Request(url=self.notice_url,
                             dont_filter=True,
                             method = 'POST',
                             callback=self.parse_notice)


    def parse_notice(self, response):
        response = json.loads(response.body.decode('utf8'))
        if not response['success']:
            return

        notice = response['data'][0]
        item = SecondBaseNoticeItem()
        item['name'] = 'binance'
        item['resource'] = 'binance.com'
        item['title'] = notice['name']
        item['url'] = notice['url']
        item['time'] = utc2local(notice['time']).strftime("%Y-%m-%d %H:%M:%S")
        item['main'] = pq(requests.get(item['url']).text)('.article-body').text()
        yield item
