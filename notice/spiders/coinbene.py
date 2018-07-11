from notice.items import SecondBaseNoticeItem, DayBaseNoticeItem
from pyquery import PyQuery as pq
import scrapy
import time
import json
import pdb
import datetime
import re


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


class OkexSpider(scrapy.Spider):
    name = 'coinbene.com'
    base_url = 'http://www.coinbene.com'
    notice_url = 'https://a.coinbene.com/content/articletitle?page=1&pageSize=1'

    def start_requests(self, ):
        yield scrapy.Request(url=self.notice_url,
                             headers={'site': 'MAIN', 'lang': 'zh_CN'},
                             dont_filter=True,
                             callback=self.parse_notice)

    def parse_notice(self, response):
        """
        Response test is json contains:
        {
            "page": 1,
            "pageSize": 1,
            "totalPage": 272,
            "totalCount": 272,
            "result": [
                {
                    "id": 647,
                    "title": "【福利】CoinBene满币将为NPXS用户空投奖励的公告",
                    "body": "<div><br></div><div>尊敬的用户：rget=\"_blank\">...
                    "author_id": 6,
                    "author_name": "李鑫",
                    "lang": "zh_CN",
                    "create_time": "2018-06-27 11:18:14",
                    "site": "MAIN"
                }
            ]
        }
        :param response:
        :return:
        """
        doc = json.loads(response.text)['result'][0]
        item = DayBaseNoticeItem()
        item['name'] = 'coinbene'
        item['resource'] = 'coinbene.com'
        item['url'] = 'http://www.coinbene.com/#/notice/detail/%s' % doc['id']
        item['time'] = doc['create_time']
        item['title'] = doc['title'].replace('\n', '')
        content = doc['body'].replace('<br />', '').replace('\t', '').replace('&nbsp;', '')
        item['main'] = re.compile('<[^>]+>').sub("", content)
        yield item