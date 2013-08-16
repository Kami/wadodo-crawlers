import re

from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.item import Item, Field


email_pattern = re.compile('([\w\-\.]+@\w[\w\-]+\.+[\w\-]+)')


class CoachInfoItem(Item):
    name = Field()
    email = Field()
    website = Field()
    location = Field()


class CraigslistSpider(CrawlSpider):
    name = 'yourtrainer.com'
    allowed_domains = ['yourtrainer.com']
    start_urls = [
        #'https://yourtrainer.com/find/personal-training/georgia/decatur',
        #'https://yourtrainer.com/find/personal-training/georgia/atlanta',
        #'https://yourtrainer.com/find/personal-training/georgia/sandy-springs',
        #'https://yourtrainer.com/find/personal-training/georgia/chamblee',
        #'https://yourtrainer.com/find/personal-training/georgia/woodstock',
        #'https://yourtrainer.com/find/personal-training/georgia/hapeville',
        #'https://yourtrainer.com/find/personal-training/georgia/macon',
        #'https://yourtrainer.com/find/personal-training/new-york/new-york',
        'https://yourtrainer.com/find/personal-training/new-york/new-rochelle',
        'https://yourtrainer.com/find/personal-training/new-jersey',
        'https://yourtrainer.com/find/personal-training/oregon',
        'https://yourtrainer.com/find/personal-training/utah',
        'https://yourtrainer.com/find/personal-training/utah',
        'https://yourtrainer.com/find/personal-training/south-carolina',
        'https://yourtrainer.com/find/personal-training/delaware',
        'https://yourtrainer.com/find/personal-training/michigan',
        'https://yourtrainer.com/find/personal-training/idaho',
        'https://yourtrainer.com/find/personal-training/tennessee',
        'https://yourtrainer.com/find/personal-training/washington',

        #'https://yourtrainer.com/find/personal-trainers/new-mexico',
        #'https://yourtrainer.com/find/personal-trainers/virginia',
        #'https://yourtrainer.com/find/personal-trainers/georgia',
        #'https://yourtrainer.com/find/personal-trainers/texas',
        #'https://yourtrainer.com/find/personal-trainers/maryland',
        #'https://yourtrainer.com/find/personal-trainers/florida',
        #'https://yourtrainer.com/find/personal-trainers/massachusetts',
        #'https://yourtrainer.com/find/personal-trainers/colorado',
        #'https://yourtrainer.com/find/personal-trainers/montana',
        #'https://yourtrainer.com/find/personal-trainers/alberta',
        #'https://yourtrainer.com/find/personal-trainers/north-carolina',
        #'https://yourtrainer.com/find/personal-trainers/illinois',
        #'https://yourtrainer.com/find/personal-trainers/ohio',
        #'https://yourtrainer.com/find/personal-trainers/kansas',
        #'https://yourtrainer.com/find/personal-trainers/arizona',
        #'https://yourtrainer.com/find/personal-trainers/rhode-island',
        #'https://yourtrainer.com/find/personal-trainers/california',
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=('/\w+\-\w+\-\d+', ),
                               restrict_xpaths=['//h3[@class="listing-name"]']),
             callback='parse_listing'),
        Rule(SgmlLinkExtractor(allow=('\?page=\d+', ),
                               restrict_xpaths=['//div[@class="pages"]'])),
    ]

    def parse_listing(self, response):
        hxs = HtmlXPathSelector(response)

        body = response.body
        name = hxs.select('//h1/text()').extract()[0]
        location = hxs.select('//h2/text()').extract()[0]

        try:
            email = email_pattern.findall(body)[0]
        except IndexError:
            return None

        item = CoachInfoItem()
        item['name'] = name
        item['email'] = email
        item['location'] = location
        return item
