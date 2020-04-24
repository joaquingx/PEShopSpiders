# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from utils.mongo_db_utils import get_collection


class ShopspidersPipeline(object):
    def __init__(self):
        self.items = list(get_collection().find({}))  # Gets mongo db in memory :scream_cat:
        self.collection = get_collection()

    def process_item(self, item, spider):
        if 'currency' not in item:
            item['currency'] = 'PEN'
        return item