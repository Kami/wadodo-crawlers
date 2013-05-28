from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from wadodo_crawlers.items import ActivityItem, ActivityItemLoader
from wadodo_crawlers.utils.flickr import get_images_for_term
from wadodo_crawlers.settings import NEVADA_BOUNDING_BOX
from wadodo_crawlers.spiders.base import FlickrCrawlSpider


# Maps parent URL to Wadodo category
URL_TO_CATEGORIES_MAP = {
    'http://www.vegas.com/attractions/museums-galleries-las-vegas/': [
        'Art',
        'Heritage',
        'Science'
    ],
    'http://www.vegas.com/attractions/recreation-las-vegas/': [
        'Adrenaline'
    ],
    'http://www.vegas.com/attractions/thrill-rides-las-vegas/': [
        'Sport',
        'Nature'
    ]
}

URL_TO_PRICE_RANGE_MAP = {
    'http://www.vegas.com/attractions/attractions-for-kids/': 'free'
}


class VegasDotComSpider(FlickrCrawlSpider):
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
        super(VegasDotComSpider, self).__init__(*args, **kwargs)
        self._nevada_bbox = ','.join(NEVADA_BOUNDING_BOX)

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

        referer = response.request.headers.get('Referer', None)

        if referer:
            # If available, set categories and price range
            if referer in URL_TO_CATEGORIES_MAP:
                l.add_value('categories', URL_TO_CATEGORIES_MAP[referer])

            if referer in URL_TO_PRICE_RANGE_MAP:
                l.add_value('price', URL_TO_PRICE_RANGE_MAP[referer])

        item = l.load_item()
        name = item['name']

        if self._flickr_api_key:
            images = get_images_for_term(self._flickr_api_key, search_term=name,
                                         bbox=self._nevada_bbox)
            image_urls = [item['url'] for item in images]
            l.add_value('image_urls', image_urls)
            item = l.load_item()

        return item
