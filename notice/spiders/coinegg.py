import scrapy
import requests
import json
import time
from pyquery import PyQuery as pq
from notice.items import SecondBaseNoticeItem
import re

# 有问题未完成
class CoineggSpider(scrapy.Spider):
    name = 'coinegg.com'
    base_url = 'https://www.coinegg.com'
    notice_url = 'https://www.coinegg.com/index/news/list'

    def start_requests(self, ):
        headers={
            "Host": "www.coinegg.com",
            "Connection": "keep-alive",
            "Content-Length": "30",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "https://www.coinegg.com",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://www.coinegg.com/gonggao/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "__cfduid=d12ece1dc1291467d31791ab00992f3fa1528450681; USER_PW=46f3d0ee6dfb83aa8ddea73168c3eab7; _ga=GA1.2.1603161473.1528450690; _gid=GA1.2.1176892498.1528450690; UM_distinctid=163dec2b2f938d-0ee1edd110ae53-737356c-1fa400-163dec2b2fa8a; lang=zh_CN; __zlcmid=mohOvEh8tssoYS; languageStyle=1; CNZZDATA1273484625=516152696-1528448084-https%253A%252F%252Fwww.coinegg.com%252F%7C1528508746; cf_clearance=d8cafa5a18901ed07c591bb8ac81d1ed3fcf4343-1528511485-900; PHPSESSID=2bf25a1d5d8850d0d6464b51d3109992; _gat_gtag_UA_108097775_1=1",
        }
        yield scrapy.FormRequest(url=self.notice_url,
                                 # method="POST",
                                 headers=headers,
                                 formdata={"limit": "0",
                                           "category": "%2Fgonggao%2F"},
                                 dont_filter=True,
                                 callback=self.parse_notice)

    def parse_notice(self, response):
        response_json = json.loads(response.body.decode('utf8'))

        if not response_json['data']:
            return

        notice = response_json['data'][0]

        item = SecondBaseNoticeItem()
        item['name'] = 'CoinEgg'
        item['resource'] = 'coinegg.com'
        item['title'] = notice['title']
        item['url'] = self.base_url + notice['category'] + str(notice['id'])

        doc_detail = pq(requests.get(item['url']).text)
        item['main'] = doc_detail('.gonggao-con').text()
        date = doc_detail('div.gonggao p.p2').text()
        year, mon, day, hour, mint, second = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)', date).groups()
        item['time'] = "%s-%s-%s %s:%s:%s" % (year, mon, day, hour, mint, second)
        yield item
