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
import urllib.parse


class AexSpider(scrapy.Spider):
    name = 'aex.com'
    base_url = "https://www.aex.com"
    notice_url = 'https://www.aex.com/notice.php'

    def start_requests(self, ):
        # headers={"Accept-Language": "zh-CN,zh;q=0.9",
        #         "Cookie": "AEX_language=zh-Hant;"}
        yield scrapy.FormRequest(url=self.notice_url,
                             # headers=headers,
                                formdata={"type":"1","page":"0"},
                             dont_filter=True,
                             callback=self.parse_item)

    def parse_item(self, response):
        response_json = json.loads(response.body.decode('utf8'))[0]

        if not response_json['title']:
            return

        item = SecondBaseNoticeItem()
        item['name'] = 'AEX'
        item['resource'] = 'aex.com'
        url_en=urllib.parse.unquote(self.base_url + response_json['url'])
        # https://www.aex.com/page/news/notice/2018/0608/en_321.html
        url=re.match(r'(.*?/)en_(.*)',url_en)
        url_ch=url.group(1)+"ch_"+url.group(2)
        item['url'] =url_ch
        print(item['url'])
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        }

        doc_detail = pq(requests.get(item['url'], verify=False,headers=headers).text)
        item['title'] = doc_detail('.header h1').text()
        item['main'] = doc_detail('.article_con').text().replace('\n','')
        date = doc_detail('div.header p span').text()
        year, mon, day, hour, mint, second = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)', date).groups()
        item['time'] = "%s-%s-%s %s:%s:%s" % (year, mon, day, hour, mint, second)
        logging.log(logging.DEBUG, '[BITFINE] Get item:', item)
        yield item
