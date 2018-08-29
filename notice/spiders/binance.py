import scrapy
import requests
import json
import time
import datetime
import re
from pyquery import PyQuery as pq
from notice.settings import BINANCE_CYCLE_TIME, CHECK_TIME_THRESHOLD
from notice.items import SecondBaseNoticeItem


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


class BinanceSpider(scrapy.Spider):
    name = 'binance.com'
    base_url = 'https://support.binance.com'
    notice_url = 'https://support.binance.com/hc/zh-cn/sections/115000202591-%E6%9C%80%E6%96%B0%E5%85%AC%E5%91%8A'
    start_urls = [
        'https://support.binance.com/hc/zh-cn/sections/115000202591-%E6%9C%80%E6%96%B0%E5%85%AC%E5%91%8A',
        'https://support.binance.com/hc/zh-cn/sections/115000106672-%E6%96%B0%E5%B8%81%E4%B8%8A%E7%BA%BF'
    ]
    # def start_requests(self, ):
    #
    #     yield scrapy.Request(url=self.notice_url,
    #                          dont_filter=True,
    #                          callback=self.parse_notice)

    def parse(self, response):
        doc = pq(response.body.decode('utf8'))
        notice = list(doc('.article-list li').items())[0]
        detail_url = notice('a').attr('href')
        notice_detail = pq(self.base_url + detail_url)

        item = SecondBaseNoticeItem()
        item['name'] = 'binance'
        item['resource'] = 'binance.com'
        item['url'] = self.base_url + detail_url
        date = notice_detail('.meta-data time').attr('datetime')
        print(date)
        # year, mon, day, hour, minit,second = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)', date).groups()

        item['time'] = utc2local(date).strftime("%Y-%m-%d %H:%M:%S")
        title = notice_detail('.article-title').text().replace('\n', '').replace('\'', '')
        item['title'] = title
        details = notice_detail('.article-body').text()
        item['main'] = details
        ls = ['上线', '上市']
        for l in ls:
            if l in title:
                sTime = re.search('将于(\d+)年(\d+)月(\d+)日(.*?)(\d+):(\d+)(.*?)上线(.*?)，', details)
                coinName = sTime.group(8)
                coinTime = "%s-%s-%s %s-%s-00" % (sTime.group(1), sTime.group(2), sTime.group(3), sTime.group(5), sTime.group(6))
                data = {
                    "shop": 'binance',
                    "coinName": coinName,
                    "dateTime": coinTime,
                    "content": details,
                }
                a = requests.post(
                    'http://47.75.122.224/filterApi.php?insertTweet=True', data=data
                )
                print(a.text)
                break
        yield item
