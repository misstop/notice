from notice.items import SecondBaseNoticeItem
from notice.settings import OKEX_CYCLE_TIME, CHECK_TIME_THRESHOLD
from pyquery import PyQuery as pq
import scrapy
import time
import json
import pdb
import datetime

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


class OkexSpider(scrapy.Spider):
    name = 'okex.com'
    base_url = 'https://support.okex.com'
    start_urls = ['https://support.okex.com/hc/zh-cn/sections/360000030652', 
            'https://support.okex.com/hc/zh-cn/sections/115000447632']

    def start_requests(self, ):
        # while True:
            for url in self.start_urls:
                yield scrapy.Request(url=url,
                                     dont_filter=True,
                                     callback=self.parse_notice)
        # time.sleep(OKEX_CYCLE_TIME)

    def parse_notice(self, response):
        doc = pq(response.body.decode('utf8'))
        notice = list(doc('.article-list li').items())[0]
        detail_url = notice('a').attr('href')
        notice_detail = pq(self.base_url + detail_url)

        item = SecondBaseNoticeItem()
        item['name'] = 'okex'
        item['resource'] = 'okex.com'
        item['url'] =  self.base_url + detail_url
        date=notice_detail('.meta-data time').attr('datetime')

        item['time'] =utc2local(date).strftime("%Y-%m-%d %H:%M:%S")

        item['title'] = notice_detail('.article-title').text().replace('\n', '').replace('\'', '')
        item['main'] = notice_detail('.article-body').text()
        yield item
