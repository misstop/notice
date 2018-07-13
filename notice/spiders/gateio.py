import scrapy
import requests
import time
from notice.items import SecondBaseNoticeItem
from pyquery import PyQuery as pq


class GateioSpider(scrapy.Spider):
    name = 'gate.io'
    url = 'https://gateio.io/articlelist/ann'
    base_url = 'https://gateio.io'
    headers = {'accept-language':'zh-CN,zh'}

    def start_requests(self, ):
        # while True:
            yield scrapy.Request(url=self.url, 
                    dont_filter=True, 
                    headers = self.headers,
                    callback=self.parse)
            # time.sleep(GATEIO_CYCLE_TIME)

    def parse(self, response):
        doc = pq(response.body)
        notice_url = list(doc('#lcontentnews a').items())[0]
        detail_resp = requests.get(self.base_url + notice_url.attr('href'), headers=self.headers)
        doc = pq(detail_resp.text)

        item = SecondBaseNoticeItem()
        item['name'] = 'gate'
        item['resource'] = 'gateio.io'
        item['url'] = self.base_url + notice_url.attr('href')
        item['title'] = doc('.dtl-title').text()
        item['time'] = doc('.new-dtl-info span').text()
        main = doc('.dtl-content')
        main.remove('style').remove('#snsshare').remove('ul')
        item['main'] = main.text()
        yield item



