from notice.items import SecondBaseNoticeItem, DayBaseNoticeItem
from pyquery import PyQuery as pq
import scrapy
import time
import json
import pdb
import datetime


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


class UexSpider(scrapy.Spider):
    name = 'uex.com'
    base_url = 'https://www.uex.com/'
    notice_url = 'https://www.uex.com/index.html'

    def start_requests(self, ):
        yield scrapy.Request(url=self.notice_url,
                             headers={'cookie': "clientCommonlanguage=zh_CN"},
                             dont_filter=True,
                             callback=self.parse)

    def parse(self, response):
        doc = pq(response.body.decode('utf8'))
        notice = list(doc('.notice span').items())[0]
        detail_url = notice('a').attr('href')
        notice_detail = pq(self.base_url + detail_url)

        item = DayBaseNoticeItem()
        item['name'] = 'uex'
        item['resource'] = 'uex.com'
        item['url'] = self.base_url + detail_url
        item['time'] = notice_detail('.time').text()
        item['title'] = notice('a').text()
        item['main'] = notice_detail('.detail-con').text()
        yield item