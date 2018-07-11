import scrapy
import requests
import json
import time
from pyquery import PyQuery as pq
from notice.items import SecondBaseNoticeItem
import datetime
import re
def string2datetime(str,format="%Y-%m-%dT%H:%M:%S+09:00"):
    return datetime.datetime.strptime(str,format)
def han2zhong(han_str):
    han_time=string2datetime(han_str)
    delta = datetime.timedelta(hours=1)
    zhong_time = han_time - delta
    return zhong_time

class UpbitSpider(scrapy.Spider):
    name = 'upbit.com'
    base_url='https://upbit.com/service_center/notice?id='
    info_url='https://api-manager.upbit.com/api/v1/notices/'
    notice_url = 'https://api-manager.upbit.com/api/v1/notices?page=1&per_page=20'

    def start_requests(self,):
            yield scrapy.Request(url=self.notice_url,
                                 dont_filter=True,
                                 callback=self.parse_notice)

    def parse_notice(self, response):
        response_json = json.loads(response.body.decode('utf8'))

        if not response_json['success']:
            return

        notice = response_json['data']['list'][0]
        item = SecondBaseNoticeItem()
        item['name'] = 'Upbit'
        item['resource'] = 'upbit.com'
        item['title'] = notice['title']
        item['url'] = self.base_url+str(notice['id'])
        item['time'] = han2zhong(notice['updated_at']).strftime("%Y-%m-%d %H:%M:%S")
        response_str = requests.get(self.info_url+str(notice['id']), verify=False)
        content = response_str.content.decode('utf-8')
        content = json.loads(content)
        if not content['success']:
            return
        body=content['data']['body']
        result, number = re.subn(r"<a.*?>", '' , body)
        result, number = re.subn(r"</a>", '' , result)
        item['main'] =result
        yield item
