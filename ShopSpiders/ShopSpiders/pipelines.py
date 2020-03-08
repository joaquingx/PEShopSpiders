# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from ShopSpiders.utils.mongo_db_utils import insert_update, get_collection


class ShopspidersPipeline(object):
    def process_item(self, item, spider):
        collection = get_collection()
        ack = insert_update(item, spider, collection)
        if ack:
            logging.log(logging.INFO, "%s inserted/updated successfully.", item)
        else:
            logging.log(logging.error, "%s not inserted", item)
        return item
