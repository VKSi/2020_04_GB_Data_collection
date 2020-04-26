# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from sothebysdiamonds.items import SothebysdiamondsItem
from scrapy.loader import ItemLoader


class RingsSpider(scrapy.Spider):
    allowed_domains = ['sothebysdiamonds.com']

    def __init__(self, text):
        self.start_urls = [f'https://www.sothebysdiamonds.com/category/{text}/']
        self.name = f'{text}'

    def parse(self, response):
        item_links = response.xpath("//div[contains(@class, 'product-block-inner')]/a/@href").extract()
        for link in item_links:
            yield response.follow(link, callback=self.parse_items)

    def parse_items(self, response: HtmlResponse):
        loader = ItemLoader(item=SothebysdiamondsItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        more_than_one_photo = response.xpath("//div[@class='detaildot detail']/a/@data-image")
        loader.add_xpath('photos', ("//span[@class='imgzoom']/img[@class='featured']/@src",
                                    "//div[@class='detaildot detail']/a/@data-image")[bool(more_than_one_photo)])
        loader.add_xpath('category', "//div[@class='breadcrumbs']/a/text()")
        loader.add_xpath('description', "//div[@class='description']/p//text()")
        yield loader.load_item()

