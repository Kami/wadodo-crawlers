import re

from scrapy.contrib.spiders import Rule
from scrapy.http import FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.item import Item, Field


email_pattern = re.compile('([\w\-\.]+@\w[\w\-]+\.+[\w\-]+)')

PROFESSIONS = [
    4,  #  Athletic Trainer
    #14,  # Golf Professional
    19,  # Martial Arts Instructor
    26,  # Nutritionist
    29,  # Personal Trainer
    35,  # Sports Coach
    36,  # Strength Coach
    38,  # Yoga teacher
]

PROFESSION = 38

class CoachInfoItem(Item):
    email = Field()
    website = Field()


class CraigslistSpider(CrawlSpider):
    name = 'chekconnect.com'
    allowed_domains = ['chekconnect.com']
    start_urls = [
        'http://www.chekconnect.com/app/findpractitioner',
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=('/app/profile\?practitionerId=\d+', )),
                               callback='parse_listing'),
        Rule(SgmlLinkExtractor(allow=('/app/searchresults\?page=\d+', ),
                               restrict_xpaths=['//a[contains(text(), "Next")]'])),
    ]

    def parse_start_url(self, response):
        base_data = {
            'name': '',
            'country': '',
            '_state': '1',
            'language': '0',
            'qualification': '0--',
            'level': '0',
            'speciality': '0',
            '_isTrainer': 'on'
        }

        data = base_data.copy()
        data['profession'] = str(PROFESSION)
        form_request = FormRequest.from_response(response,
            formdata=data)
        return form_request

        requests = []
        for profession in PROFESSIONS:
            data = base_data.copy()
            data['profession'] = str(PROFESSION)
            form_request = FormRequest.from_response(response,
                formdata=data)
            requests.append(form_request)
        return requests

    def parse_noop(self, request):
        hxs = HtmlXPathSelector(response)
        return None

    def parse_listing(self, response):
        hxs = HtmlXPathSelector(response)
        email = hxs.select('//div[@id="emailAddress"]/div[2]/text()').extract()
        website = hxs.select('//div[@id="website"]/div/a/@href').extract()

        if not email:
            return

        item = CoachInfoItem()
        item['email'] = email[0]

        if website:
            item['website'] = website[0]

        return item
