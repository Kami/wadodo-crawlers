from scrapy.contrib.spiders import CrawlSpider

__all__ = [
    'FlickrCrawlSpider'
]


class FlickrCrawlSpider(CrawlSpider):
    def __init__(self, *args, **kwargs):
        flickr_api_key = kwargs.pop('flickr_api_key', None)

        self._flickr_api_key = flickr_api_key
        super(FlickrCrawlSpider, self).__init__(*args, **kwargs)
