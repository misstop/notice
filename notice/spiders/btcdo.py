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


class BilaxySpider(scrapy.Spider):
    name = 'btcdo.com'
    base_url = "https://www.btcdo.com"
    notice_url = 'https://www.btcdo.com/apis/user/findNoticeList'

    def start_requests(self, ):
        yield scrapy.Request(url=self.notice_url,
                             dont_filter=True,
                             method='POST',
                             headers={'Content-Type': 'application/json'},
                             body=json.dumps({"offset": 0, "maxResults": 1, "languageId": 1}),
                             callback=self.detail_parse,)

    def detail_parse(self, response):
        """
        Response test is json contains:
           [
                {
                    "id": 100114,
                    "createdAt": 1529136845456,
                    "updatedAt": 1529171287662,
                    "columnId": 5,
                    "languageId": 1,
                    "beginTime": 1529107200000,
                    "endTime": 1556668800000,
                    "sortsId": 9945,
                    "userId": 100020,
                    "content": "<p style=\"line-height: 2em;\">雅黑, &quot;Microsoft YaHei&quot;..."
                    "title": "【公告】币为Btcdo已完成更换USDT合约",
                    "status": 1
                }
            ]
        :param response:
        :return:
        """
        l_last = json.loads(response.text)[0]
        tid = l_last['id']
        item = SecondBaseNoticeItem()
        item['name'] = 'btcdo'
        item['resource'] = 'btcdo.com'
        item['url'] = 'https://www.btcdo.com/index/notice/noticeDetail?id=%s' % tid
        item['title'] = l_last['title']
        content = l_last['content'].replace('\t', '').replace('&nbsp;', '')
        item['main'] = re.compile('<[^>]+>').sub("", content)
        x = time.localtime(l_last['beginTime'] // 1000)
        str_time = time.strftime('%Y-%m-%d %H:%M:%S', x)
        item['time'] = str_time
        logging.log(logging.DEBUG, '[BTCDO] Get item:', item)
        yield item