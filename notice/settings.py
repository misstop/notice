# -*- coding: utf-8 -*-

# Scrapy settings for notice project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'notice'

SPIDER_MODULES = ['notice.spiders']
NEWSPIDER_MODULE = 'notice.spiders'
COMMANDS_MODULE = 'notice.commands'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'notice (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
   # 'notice.middlewares.NoticeSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'notice.middlewares.BinanceDownloadMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'notice.pipelines.NoticePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 0
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# for spider
CHECK_TIME_THRESHOLD = 24 * 60 * 60 # 时间差阀值

# for twitter
TWEEN_COUNT = 1  # api调用时一次获取的数量

# day base
BITFINEX_CYCLE_TIME =  60 * 60
KUCOIN_CYCLE_TIME =  60 * 60

# second base
SECOND_BASE_CYCLE_IME = 5 * 60
HUOBIPRO_CYCLE_TIME = 5 * 60
OKEX_CYCLE_TIME = 5 * 60
BINANCE_CYCLE_TIME = 5 * 60
GATEIO_CYCLE_TIME = 5 * 60
BIBOX_CYCLE_TIME =  5 * 60
BIGONE_CYCLE_TIME = 5 * 60
COINYEE_CYCLE_TIME = 5 * 60
TOPBTC_CYCLE_TIME = 5 * 60
OTCBTC_CYCLE_TIME = 5 * 60

# for text
# MONGO_HOST = '192.168.33.130'
# for db
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_USER = 'chenbin'
MONGO_PASSWORD = 'chenbin'
MONGO_DB = 'dianmo'
MONGO_NOTICE_COLLECTION = 'notice'

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_TWITTER_USERS_KEY = 'twitter_users'

# 超时时间
DOWNLOAD_TIMEOUT = 20
# 重试次数
RETRY_TIMES = 0
# 日志
# LOG_FILE = 'notice.log'
# LOG_LEVEL = 'INFO'
