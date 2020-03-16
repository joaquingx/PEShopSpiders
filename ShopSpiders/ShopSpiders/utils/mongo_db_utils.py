"""Utilitary functions for mongodb."""

from pymongo import MongoClient
from pymongo.collection import Collection

from settings import MONGO_COLLECTION, MONGO_DB, MONGO_URI
from utils.normalization import normalize


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


def insert_update(document: dict, spider, collect: Collection) -> bool:
    """name will be searched on db, if found then just update item otherwise create a new one."""
    document['name'] = normalize(document['name'])
    return collect.update_one({'name': document['name']}, transform_to_update(document, spider.name), upsert=True).acknowledged
