# Scrapy settings for wadodo_crawlers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import random

BOT_NAME = 'wadodo_crawlers'

SPIDER_MODULES = ['wadodo_crawlers.spiders']
NEWSPIDER_MODULE = 'wadodo_crawlers.spiders'

USER_AGENTS = [
    'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
    'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.7.4; U; en) Presto/2.10.229 Version/11.62',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.10.229 Version/11.62',
]

ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline']
IMAGES_STORE = 'downloaded_images/'

# Optimal settings for not getting banned
COOKIES_ENABLED = False
DOWNLOAD_DELAY = 2
USER_AGENT = random.choice(USER_AGENTS)

# Misc
# Bounding box for Nevada
# http://www.flickr.com/places/info/2347587
NEVADA_BOUNDING_BOX = [
  '-120.0058',
  '35.0023',
  '-114.0394',
  '42.0018'
]
