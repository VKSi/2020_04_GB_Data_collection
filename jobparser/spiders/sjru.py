# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['russia.superjob.ru']

    def __init__(self, text):
        self.start_urls = [
            f'https://russia.superjob.ru/vacancy/search/?keywords={text}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_links = response.xpath("//div[@class='_3mfro CuJz5 PlM3e _2JVkc _3LJqf']/a/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parce)

    def vacancy_parce(self, response:HtmlResponse):
        link1 = response.url
        name1 = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract()
        compensation1 = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        employer1 = response.xpath("//h2[@class='_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI']/text()").extract()
        yield JobparserItem(name= name1, compensation= compensation1, employer= employer1, link= link1)