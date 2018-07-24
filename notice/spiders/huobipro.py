from notice.items import SecondBaseNoticeItem
import requests
from notice.settings import HUOBIPRO_CYCLE_TIME, CHECK_TIME_THRESHOLD
from pyquery import PyQuery as pq
import scrapy
import time
import json


class HuobiproSpider(scrapy.Spider):
    name = 'huobipro.com'
    base_url='https://www.huobipro.com/zh-cn/notice_detail/?id='
    notice_detail_url = 'https://www.huobipro.com/-/x/hb/p/api/contents/pro/notice/'
    notice_url = 'https://www.huobipro.com/-/x/hb/p/api/contents/pro/list_notice?limit=20&language=zh-cn'

    def start_requests(self, ):
        # while True:
            yield scrapy.Request(url=self.notice_url,
                                 dont_filter=True,
                                 callback=self.parse_notice)
            # time.sleep(HUOBIPRO_CYCLE_TIME)

    def parse_notice(self, response):
        response_json = json.loads(response.body.decode('utf8'))
        if not response_json['success']:
            return

        notice = response_json['data']['items']
        toplist = []
        for data in notice:
            if data['topNotice']:
                toplist.append(data)
        notice = toplist[0]

        item = SecondBaseNoticeItem()
        item['name'] = 'huobipro'
        item['resource'] = 'huobipro.com'
        item['title'] = notice['title']
        item['url'] = self.base_url+str(notice['id'])
        timestamp = notice['created'] / 1000
        timestamp =  int(float(timestamp))
        item['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

        response_str = requests.get(self.notice_detail_url + str(notice['id']))

        content = response_str.content.decode('utf-8')
        content = json.loads(content)
        if not content['success']:
            return
        item['main'] = pq(content['data']['content']).text()
        print("第一个item")
        yield item
        # --------------------------------------------------------------------
        response_json = json.loads(response.body.decode('utf8'))
        if not response_json['success']:
            return

        notice = response_json['data']['items']
        nottoplist = []
        for data in notice:
            if not data['topNotice']:
                nottoplist.append(data)
        notice = nottoplist[0]

        item = SecondBaseNoticeItem()
        item['name'] = 'huobipro'
        item['resource'] = 'huobipro.com'
        item['title'] = notice['title']
        item['url'] = self.base_url + str(notice['id'])
        timestamp = notice['created'] / 1000
        timestamp = int(float(timestamp))
        item['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

        response_str = requests.get(self.notice_detail_url + str(notice['id']))

        content = response_str.content.decode('utf-8')
        content = json.loads(content)
        if not content['success']:
            return
        item['main'] = pq(content['data']['content']).text()
        print("第二个item")
        yield item


