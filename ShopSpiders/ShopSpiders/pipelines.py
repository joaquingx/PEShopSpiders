# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime, timezone
from pymongo.collection import Collection
from scrapy.spiders import Spider
from utils.mongo_db_utils import get_collection, insert_one


class ShopspidersPipeline(object):
    collection: Collection

    def __init__(self):
        self.collection = get_collection()

    @staticmethod
    def aggregate_data(item: dict, spider: Spider):
        if 'currency' not in item:
            item['currency'] = 'PEN'
        item['timestamp'] = datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")
        item['spider'] = spider.name

    def process_item(self, item: dict, spider: Spider):
        self.aggregate_data(item, spider)
        insert_one(item, self.collection)
        return item
