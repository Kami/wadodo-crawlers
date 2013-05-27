from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join

from wadodo_scrapers.utils import replace_nbrs, JoinAddress


class ActivityItem(Item):
    source_url = Field()

    name = Field()
    address = Field()
    phone_number = Field()
    website = Field()
    description = Field()
    time_needed = Field()
    price = Field()


class ActivityItemLoader(XPathItemLoader):
    default_output_processor = TakeFirst()

    name_out = TakeFirst()
    address_in = MapCompose(unicode.strip)
    address_out = JoinAddress()
    description_in = MapCompose(replace_nbrs)
    description_out = Join('\n')
    time_needed_out = TakeFirst()
    price_out = TakeFirst()
