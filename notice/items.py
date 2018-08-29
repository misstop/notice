# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecondBaseNoticeItem(scrapy.Item):
    name = scrapy.Field()  # 类别的唯一标识
    title = scrapy.Field()  # 标题
    resource = scrapy.Field()  # 来源
    # XXXX-XX-XX XX:XX:XX
    time = scrapy.Field()  # 时间
    url = scrapy.Field()  # url
    main = scrapy.Field()  # 内容
    # coinTime = scrapy.Field()   # 上币时间
    # coinName = scrapy.Field()   # 上币的名字


class DayBaseNoticeItem(scrapy.Item):
    name = scrapy.Field()  # 唯一标识
    summary = scrapy.Field()
    title = scrapy.Field()  # 标题
    resource = scrapy.Field()  # 来源
    time = scrapy.Field()  # 时间
    url = scrapy.Field()  # url
    main = scrapy.Field()  # 内容
    # coinTime = scrapy.Field()   # 上币时间
    # coinName = scrapy.Field()   # 上币的名字
