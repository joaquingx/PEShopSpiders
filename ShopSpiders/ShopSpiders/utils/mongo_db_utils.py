"""Utilitary functions for mongodb."""
import jaro
from pymongo import MongoClient
from pymongo.collection import Collection
import logging


from scrapy.spiders import Spider
from settings import MONGO_COLLECTION, MONGO_DB, MONGO_URI
from utils.normalization import normalize

logger = logging.getLogger(__name__)


def get_collection() -> Collection:
    """Returns relevant collection."""
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db[MONGO_COLLECTION]


def transform_to_update(document: dict, name: str):
    """Returns a valid update document."""
    dict_updt = {'$set': {}}
    for k, i in document.items():
        if k != 'name':
            dict_updt['$set'].update({
                f'{k}s.{name}': i,
            })
    return dict_updt


def get_most_similar(items: list, document: dict, threshold=0.895):
    """Search for most similar in items. Also, item should be at least threshold similar to be considered."""
    similar, ratio = None, 0
    for item in items:
        if 'name' in item:
            similarity = jaro.jaro_winkler_metric(normalize(item['name']), normalize(document['name']))
            # print(item['name'], document['name'], similarity)
            if similarity > threshold and similarity > ratio:
                similar, ratio = item['_id'], similarity
    return similar, ratio


def insert_update(document: dict, spider: Spider, collect: Collection, items: list) -> bool:
    """Name will be searched on db, if found then just update item otherwise create a new one."""
    obj_id, ratio = get_most_similar(items, document)
    if obj_id:
        logger.info('*************%s found a similar one: %s, ratio: %s*************************',
                    document['name'], collect.find_one({"_id": obj_id}), str(ratio))
    obj_id = 0 if not obj_id else obj_id
    return collect.update_one({'_id': obj_id}, transform_to_update(document, spider.name), upsert=True).acknowledged
