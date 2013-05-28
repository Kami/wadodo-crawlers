from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from wadodo_crawlers.items import ActivityItem, ActivityItemLoader
from wadodo_crawlers.utils.flickr import get_images_for_term
from wadodo_crawlers.settings import NEVADA_BOUNDING_BOX


class VegasDotComSpider(CrawlSpider):
    name = 'vegas.com'
    allowed_domains = ['vegas.com']
    start_urls = [
        'http://www.vegas.com/attractions/attractions-for-kids/',
        'http://www.vegas.com/attractions/free-attractions-las-vegas/',
        'http://www.vegas.com/attractions/museums-galleries-las-vegas/',
        'http://www.vegas.com/attractions/recreation-las-vegas/',
        'http://www.vegas.com/attractions/thrill-rides-las-vegas/',
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=('/attractions/.+/index\.html', ),
                               restrict_xpaths=['//a[@class="standard-info-title-link"]']), callback='parse_activity'),
    ]

    def __init__(self, *args, **kwargs):
        flickr_api_key = kwargs.pop('flickr_api_key', None)

        if flickr_api_key is None:
            raise ValueError('Missing flickr_api_key argument')

        self._flickr_api_key = flickr_api_key
        self._nevada_bbox = ','.join(NEVADA_BOUNDING_BOX)

        super(VegasDotComSpider, self).__init__(*args, **kwargs)

    def parse_activity(self, response):
        l = ActivityItemLoader(item=ActivityItem(), response=response)
        l.add_xpath('name', '//h1[@class="main-page-title"]/text()')

        # Address
        l.add_xpath('address', '//div[@class="product-summary-list-box"]/div[1]/text()')

        # City
        l.add_xpath('address', '//div[@id="product-location"]/div/div[@class="street-address"]/following-sibling::div/span[@class="locality"]/text()')

        # State
        l.add_xpath('address', '//div[@id="product-location"]/div/div[@class="street-address"]/following-sibling::div/abbr[@class="region"]/text()')

        # Zip Code
        l.add_xpath('address', '//div[@id="product-location"]/div/div[@class="street-address"]/following-sibling::div/span[@class="postal-code"]/text()')
        l.add_xpath('description', '//div[@class="product-details-description layout-module expandable collapsed"]/p/text()')
        l.add_xpath('time_needed', '//strong[contains(text(), "Tour Length: ")]/following-sibling::div/text()')
        l.add_xpath('price', '//div[@class="fromprice-price"]/text()')

        l.add_value('source_url', response.url)

        item = l.load_item()
        name = item['name']

        images = get_images_for_term(self._flickr_api_key, search_term=name,
                                     bbox=self._nevada_bbox)
        image_urls = [item['url'] for item in images]
        l.add_value('image_urls', image_urls)

        item = l.load_item()
        return item
