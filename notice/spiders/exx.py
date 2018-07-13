import scrapy
import pdb
import json
import time
from notice.items import SecondBaseNoticeItem
from pyquery import PyQuery as pq
import requests

class ExxSpider(scrapy.Spider):
    name = 'exx.com'
    list_url = 'https://main.exx.com/darkcore/web/problem/ProblemAction/getProblemListTop?problemType=1&problCategor=102'
    detail_url = 'https://www.exx.com/blog/display?type=102&id={id}'

    def start_requests(self, ):
        # while True:
            yield scrapy.Request(self.list_url,
                    dont_filter=True,
                    callback=self.parse)
        # time.sleep(SECOND_BASE_CYCLE_IME)

    def parse(self, response):
        data = json.loads(response.body.decode('utf8'))
        id = data['datas']['titelList'][0]['id']
        detail_resp = requests.get(self.detail_url.format(id=id))
        doc = pq(detail_resp.text)
        item = SecondBaseNoticeItem()
        item['name'] = 'exx'
        item['resource'] = 'exx.com'
        item['url'] = self.detail_url.format(id=id)
        title = doc('#blog h2')
        item['time'] = doc('#blog .time').text().split('：', 1)[-1]
        title.remove('p')
        item['title'] = title.text()
        item['main'] = doc('#blog .blog-info').text()
        yield item


