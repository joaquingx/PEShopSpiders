# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from utils.mongo_db_utils import insert_update, get_collection
from utils.similarity import load_dict_model, get_index, similarity


class ShopspidersPipeline(object):
    def __init__(self):
        self.dictionary, self.model = load_dict_model()
        self.corpus = [document['name'] for document in list(get_collection().find({}))]

    def process_item(self, item, spider):
        # collection = get_collection()
        index = get_index(self.corpus, self.dictionary, self.model)
        similarity(self.corpus, item['name'], self.dictionary, self.model, index)
        # ack = insert_update(item, spider, collection)
        # if ack:
        #     logging.log(logging.INFO, "%s inserted/updated successfully.", item)
        # else:
        #     logging.log(logging.error, "%s not inserted", item)
        return item
