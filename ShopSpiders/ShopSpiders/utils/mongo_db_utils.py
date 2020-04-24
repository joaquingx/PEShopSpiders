"""Utilitary functions for mongodb."""
from pymongo import MongoClient
from pymongo.collection import Collection
import logging

from settings import MONGO_COLLECTION, MONGO_DB, MONGO_URI

logger = logging.getLogger(__name__)


def get_collection() -> Collection:
    """Returns relevant collection."""
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db[MONGO_COLLECTION]


def insert_one(document: dict, collect: Collection) -> bool:
    inserted_result = collect.insert_one(document)
    if not inserted_result.acknowledged:
        logger.warning("%s could not be inserted!", str(document))
    else:
        logger.info('%s inserted', inserted_result.inserted_id)
    return inserted_result
