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
    name = 'bilaxy.com'
    base_url = "https://bilaxy.com"
    notice_url = 'https://bilaxy.com/api/v1/articleList?type=1&page=1&pageSize=10'

    def start_requests(self, ):
        yield scrapy.Request(url=self.notice_url,
                             dont_filter=True,
                             callback=self.title_parse)

    def title_parse(self, response):
        """
        Response test is json contains:
            {
                code: 200,
                data: [
                        {
                        id: 111,
                        title: "gochain（GO)现已上线币系",
                        enTitle: "gochain(GO) is listed on Bilaxy",
                        top: false,
                        createTime: 1528563029000,
                        },

                    ],
                totalCount: 46,
                page: 0,
                msg: null,
                id: null,
            }
        :param response:
        :return:
        """
        l_last = json.loads(response.text)['data'][0]
        tid = l_last['id']
        item = SecondBaseNoticeItem()
        item['name'] = 'Bilaxy'
        item['resource'] = 'bilaxy.com'
        item['url'] = 'https://bilaxy.com/news/detail?id=%s' % tid
        real_url = 'https://bilaxy.com/api/v1/articleDetail?id=%s' % tid
        res_detail = requests.get(real_url).text
        detail = json.loads(res_detail)['data']['content']

        # 此时返回所有title和该id的content
        item['title'] = detail['title']
        content = detail['content'].replace('<br />', '').replace('\t', '').replace('&nbsp;', '')
        item['main'] = re.compile('<[^>]+>').sub("", content)
        x = time.localtime(detail['createTime'] / 1000)
        str_time = time.strftime('%Y-%m-%d %H:%M:%S', x)
        item['time'] = str_time
        logging.log(logging.DEBUG, '[BILAXY] Get item:', item)
        yield item
