import scrapy
import requests
import json
import time
from pyquery import PyQuery as pq
from notice.items import SecondBaseNoticeItem


class HadaxSpider(scrapy.Spider):
    name = 'hadax.com'
    base_url='https://www.hadax.com/zh-cn/notice_detail/?id='
    info_url='https://content.hadax.com/p/api/contents/hadax/notice/'
    notice_url = 'https://content.hadax.com/p/api/contents/hadax/list_notice?limit=10&language=zh-cn'

    def start_requests(self,):
        # while True:
            yield scrapy.Request(url=self.notice_url,
                                 dont_filter=True,
                                 callback=self.parse_notice)
            # time.sleep(HADAX_CYCLE_TIME)
            # time.sleep(1)
    def parse_notice(self, response):
        response_json = json.loads(response.body.decode('utf8'))

        if not response_json['success']:
            return

        notice = response_json['data']['items']
        toplist=[]
        for data in notice:
            if data['topNotice']:
                toplist.append(data)
        notice=toplist[0]

        item = SecondBaseNoticeItem()
        item['name'] = 'HADAX'
        item['resource'] = 'hadax.com'
        item['title'] = notice['title']
        item['url'] = self.base_url+str(notice['id'])
        timestamp = notice['created'] / 1000
        timestamp = int(float(timestamp))
        item['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

        response_str = requests.get(self.info_url+str(notice['id']))
        content = response_str.content.decode('utf-8')
        content = json.loads(content)
        if not content['success']:
            return
        item['main'] = pq(content['data']['content']).text()
        print("第一个item")
        yield item

        # 非置顶-------------------------------------------------------
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
        item['name'] = 'HADAX'
        item['resource'] = 'hadax.com'
        item['title'] = notice['title']
        item['url'] = self.base_url+str(notice['id'])
        timestamp = notice['created'] / 1000
        timestamp = int(float(timestamp))
        item['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

        response_str = requests.get(self.info_url+str(notice['id']))
        content = response_str.content.decode('utf-8')
        content = json.loads(content)
        if not content['success']:
            return
        item['main'] = pq(content['data']['content']).text()
        print("第二个item")
        yield item