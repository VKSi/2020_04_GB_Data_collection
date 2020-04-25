# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose


def links_cleaner(link):
    return (link, f'http:{link}')[link[:2] == '//']


def take_second(field):
    return field[1]


class SothebysdiamondsItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(links_cleaner))
    category = scrapy.Field()
    collection = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    place = scrapy.Field()
