# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, text):
        self.start_urls = [
            f'https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text={text}&showClusters=false']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()

        vacancy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parce)

        yield response.follow(next_page, callback=self.parse)

    def vacancy_parce(self, response:HtmlResponse):
        link1 = response.url
        name1 = response.xpath("//div[contains(@class, 'vacancy-title')]/h1//text()").extract()
        compensation1 = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        employer1 = response.xpath("//a[contains(@data-qa, 'vacancy-company-name')]/span/text()").extract()
        yield JobparserItem(name= name1, compensation= compensation1, employer= employer1, link= link1)