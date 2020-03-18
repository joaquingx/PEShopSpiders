# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from utils.mongo_db_utils import insert_update, get_collection
# from utils.similarity import load_dict_model, get_index, similarity
import jaro


class ShopspidersPipeline(object):
    def __init__(self):
        self.items = list(get_collection().find({}))  # Gets mongo db in memory :scream_cat:
        self.collection = get_collection()

    def process_item(self, item, spider):
        ack = insert_update(item, spider, get_collection(), self.items)
        if ack:
            logging.log(logging.INFO, "%s inserted/updated successfully.", item)
        else:
            logging.log(logging.error, "%s not inserted", item)
        return item