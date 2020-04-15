# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose,Join
from w3lib.html import remove_tags

def remove_quotations(val):
    return val.replace(u"\u201c",'').replace(u"\u201d",'').replace(u"\u2019","'").replace(u"\u2014","-")

class HealthLineItem(scrapy.Item):
    blogTitle=scrapy.Field(
        input_processor=MapCompose(str.strip,remove_quotations,remove_tags),
        output_processor=TakeFirst()
    )
    # blogText=(scrapy.Field(
    #     input_processor=MapCompose(str.strip,remove_quotations,remove_tags),
    #     output_processor=TakeFirst()
    # )
    blogText=scrapy.Field(
        input_processor=MapCompose(str.strip,remove_quotations),
        output_processor=Join()
    )
    source=scrapy.Field()
    keyword=scrapy.Field()
    link=scrapy.Field()
