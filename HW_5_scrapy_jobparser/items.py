# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    compensation = scrapy.Field()
    employer = scrapy.Field()
    compensation_min = scrapy.Field()
    compensation_max = scrapy.Field()
    compensation_currency = scrapy.Field()



