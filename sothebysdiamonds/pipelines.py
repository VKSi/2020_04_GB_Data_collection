# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class SothebysdiamondsPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.diamonds

    def process_item(self, item, spider):
        if len(item['category']) > 1:
            item['collection'] = item['category'][1]
            if item['collection'][-2:] == ' >':
                item['collection'] = item['collection'][:-2]
        item['category'] = item['category'][0]
        item['category'] = item['category'][2:]
        item['price'] = item['description'][1]
        item['place'] = item['description'][3]
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class SothebysdiamondsPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        self.item_name = item['name']
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        directory_name = self.item_name
        image_name = str(request.url).split('/')[-1]
        image_name = image_name[:image_name.find('.')]
        head_directory = self.spiderinfo.spider.name
        file_name = f'{head_directory}/{directory_name}/{image_name}.jpg'
        return file_name

    def item_completed(self, results, item, info):
        if results[0]:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
