import re

from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.item import Item, Field


email_pattern = re.compile('([\w\-\.]+@\w[\w\-]+\.+[\w\-]+)')


class CoachInfoItem(Item):
    email = Field()
    website = Field()


class CraigslistSpider(CrawlSpider):
    name = 'craigslist.com'
    #allowed_domains = ['newyork.craigslist.org']
    start_urls = [
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=('/.+?/lss/\d+\.html', )),
                               callback='parse_listing'),
        Rule(SgmlLinkExtractor(allow=('\?s=\d{3}', ),
                               restrict_xpaths=['//span[@class="nplink next"]'])),
    ]

    def parse_listing(self, response):
        body = response.body
        emails = email_pattern.findall(body)
        emails = set([e for e in emails if 'serv.craigslist' not in e])

        items = []

        for email in emails:
            item = CoachInfoItem()
            item['email'] = email
            items.append(item)

        return items
