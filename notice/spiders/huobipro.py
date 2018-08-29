from notice.items import SecondBaseNoticeItem
import requests
from notice.settings import HUOBIPRO_CYCLE_TIME, CHECK_TIME_THRESHOLD
from pyquery import PyQuery as pq
import scrapy
import time
import json
import re


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
        details = pq(content['data']['content']).text()
        item['main'] = details
        print("第一个item")
        ls = ['上线', '全球首发']
        for l in ls:
            if l in notice['title']:
                c = notice['title'].split(l)
                sTime = re.search(r'(\d+)月(\d+)日(\d+):(\d+)', c[0])
                coinName = c[1]
                coinTime = "2018-%s-%s %s-%s-00" % (sTime.group(1), sTime.group(2), sTime.group(3), sTime.group(4))
                data = {
                    "shop": 'huobipro',
                    "coinName": coinName,
                    "dateTime": coinTime,
                    "content": details,
                }
                requests.post(
                    'http://47.75.122.224/filterApi.php?insertTweet=True', data=data
                )
                break
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
        details = pq(content['data']['content']).text()
        item['main'] = details
        print("第二个item")
        ls = ['上线', '全球首发']
        for l in ls:
            if l in notice['title']:
                c = notice['title'].split(l)
                sTime = re.search(r'(\d+)月(\d+)日(\d+):(\d+)', c[0])
                coinName = c[1]
                coinTime = "2018-%s-%s %s-%s-00" % (sTime.group(1), sTime.group(2), sTime.group(3), sTime.group(4))
                data = {
                    "shop": 'huobipro',
                    "coinName": coinName,
                    "dateTime": coinTime,
                    "content": details,
                }
                requests.post(
                    'http://47.75.122.224/filterApi.php?insertTweet=True', data=data
                )
                break
        yield item


