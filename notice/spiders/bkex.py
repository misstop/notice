import logging
import re
import datetime
from notice.items import SecondBaseNoticeItem
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
    name = 'bkex.com'
    base_url = "https://www.bkex.com"
    notice_url = 'https://www.bkex.com/api/announcement/search/1/page/1/20'

    def start_requests(self, ):
        yield scrapy.Request(url=self.notice_url,
                             dont_filter=True,
                             callback=self.detail_parse)

    def detail_parse(self, response):
        """
        Response test is json contains:
           {
            msg: null,
            code: 0,
            data:
                {
                totalCount: 23,
                list: [
                        {
                        id: 99,
                        userName: null,
                        language: 1,
                        title: "关于币客BKEX 6月20日BKK赠送和分红公告",
                        content: "<table> <tbody> <tr> <td width="194"> <p>昨日平台总成交额</p>..."
                        sorting: 1,
                        createTime: 1529566192338,
                        updateTime: null,
                        status: 1,
                        tag: null,
                        readednum: 0,
                        },
                        ...
                    ]
                }
            }
        :param response:
        :return:
        """
        l_last = json.loads(response.text)['data']['list'][0]
        tid = l_last['id']
        item = SecondBaseNoticeItem()
        item['name'] = 'bkex'
        item['resource'] = 'bkex.com'
        item['url'] = 'https://www.bkex.com/#/notice/detail/%s' % tid
        item['title'] = l_last['title']
        content = l_last['content'].replace('\t', '').replace('&nbsp;', '')
        item['main'] = re.compile('<[^>]+>').sub("", content)
        x = time.localtime(l_last['createTime'] // 1000)
        str_time = time.strftime('%Y-%m-%d %H:%M:%S', x)
        item['time'] = str_time
        logging.log(logging.DEBUG, '[BKEX] Get item:', item)
        yield item
