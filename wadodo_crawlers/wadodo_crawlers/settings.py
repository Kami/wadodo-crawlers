# Scrapy settings for wadodo_crawlers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'wadodo_crawlers'

SPIDER_MODULES = ['wadodo_crawlers.spiders']
NEWSPIDER_MODULE = 'wadodo_crawlers.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0'
DOWNLOAD_DELAY = 1

ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline']
IMAGES_STORE = 'downloaded_images/'
