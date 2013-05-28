from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader.processor import Identity

from wadodo_crawlers.utils.misc import replace_nbrs, JoinAddress


class ActivityItem(Item):
    name = Field()
    categories = Field()
    address = Field()
    phone_number = Field()
    website = Field()
    description = Field()
    time_needed = Field()
    price = Field()

    source_url = Field()
    image_urls = Field()
    images = Field()


class ActivityItemLoader(XPathItemLoader):
    default_output_processor = TakeFirst()

    name_out = TakeFirst()
    categories_out = Identity()
    address_in = MapCompose(unicode.strip)
    address_out = JoinAddress()
    description_in = MapCompose(replace_nbrs)
    description_out = Join('\n')
    time_needed_out = TakeFirst()
    price_out = TakeFirst()
    image_urls_out = Identity()
    images = Identity()
