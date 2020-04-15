# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogscraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    dateCreated = scrapy.Field()
    blogText = scrapy.Field()
    source=scrapy.Field()
    keyword=scrapy.Field()
    link=scrapy.Field()
    pass
