import time
import logging
from scrapy.commands import ScrapyCommand


class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Run all of the spiders'

    def run(self, args, opts):
        spider_list = self.crawler_process.spiders.list()
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
            # logging.info("%s开始抓取 时间戳%s" % (name, time.time()))
            # print("%s开始抓取 时间戳%s" % (name, time.time()))
        self.crawler_process.start()
