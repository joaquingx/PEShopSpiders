"""PAUSED: Machine learning implementation for similarities."""
import argparse
import json
import time
import random
import sys
from os import path
import pickle
from clean import get_stop_words, remove_stop_words
from normalization import normalize
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import SparseMatrixSimilarity
from normalization import normalize
from typing import Generator, List
from pymongo import MongoClient
from pymongo.collection import Collection

from product_object import get_product_objects

MONGO_URI = 'mongodb+srv://user1:user1@cluster0-lnitk.gcp.mongodb.net/test?retryWrites=true&w=majority'
MONGO_DB = 'shop-raw-results'
MONGO_COLLECTION = 'results'


def get_word_ngram(doc: str, n: int) -> List[str]:
    word_list = doc.split(' ')
    word_ans = []
    for i in range(len(word_list)):
        word_ans.append(' '.join(word_list[i:i+n]))
    return word_ans


def get_char_ngram(doc: str, n: int) -> List[str]:
    char_ans = []
    for i in range(len(doc)-n+1):
        char_ans.append(doc[i:i+n])
    return char_ans


def get_db_in_memory(doc_list: List[dict], stop_words: List[str]):
    for item in doc_list:
        normalized_item = remove_stop_words(normalize(item.get('name', 'invalid')), stop_words)
        try:
            item['normalized_name'] = normalized_item
        except:
            print(f"{item} has no name field")
        else:
            yield item


def get_raw_corpus(doc_list: List[dict], stop_words: List[str]) -> Generator[dict, None, None]:
    """Clean documents, only return unique items."""
    unique_words = []
    spider = []
    for item in doc_list:
        normalized_item = remove_stop_words(normalize(item.get('name', 'invalid')), stop_words)
        if normalized_item not in unique_words:
            unique_words.append(normalized_item)
            spider.append(item.get('spider', '123'))
            item['name'] = normalized_item
            yield item
        else:
            idx = unique_words.index(normalized_item)
#             if spider[idx] != item['spider']:
#                 print(f'Item ({normalized_item}:{unique_words[idx]}) share product name!, spiders({item["spider"]},{spider[idx]})')


def get_cook_corpus(raw_corpus: Generator[dict, None, None], ngram) -> Generator[List[str], None, None]:
    yield from (get_char_ngram(doc['name'], ngram) for doc in raw_corpus)


def get_collection(db, collection):
    client = MongoClient(MONGO_URI)
    db = client[db]
    return db[collection]


def get_universe(doc_list: List[str]):
    spiders = []
    for i in doc_list:
        spiders.append(i['spider'])
    return set(spiders)


def save_artifact():
    arg_parser = argparse.ArgumentParser(
        description='Save a similarity artifact like corpus, model, index',
    )
    arg_parser.add_argument("artifact", help="What artifact you want to save")
    arg_parser.add_argument("in_path", help="Input path, e.g. for a index the input MUST be a model.")
    arg_parser.add_argument("out_path", help="Output path")
    arg_parser.add_argument("--train_data", help="Data to train, OPTIONAL for index artifacts if not provided will use corpus.txt",
                            default="corpus.txt")
    arg_parser.add_argument("--dict_len", help="Index len, default 2120, REALLY HARDCODED OMG, NOT REAL PROGRAMMER WILL DO THIS ASHAMED ;'(",
                            default=26612)
    arg_parser.add_argument("--ngram", default=3)

    save_args = arg_parser.parse_args(sys.argv[2:])
    ngram = int(save_args.ngram)
    if save_args.artifact == 'db_clean':
        documents = pickle.load(open(save_args.in_path, 'rb'))
        stop_words = get_stop_words()
        db = get_db_in_memory(documents, stop_words)
        pickle.dump(list(db), open(save_args.out_path, 'wb'))
        print(f"Clean DB Saved in {save_args.out_path}")

    if save_args.artifact == 'raw_corpus':
        documents = pickle.load(open(save_args.in_path, 'rb'))
        stop_words = get_stop_words()
        raw_corpus = list(get_raw_corpus(documents, stop_words))
        pickle.dump(raw_corpus, open(save_args.out_path, 'wb'))
        print(f"Raw corpus saved in {save_args.out_path}")

    if save_args.artifact == 'cook_corpus':
        print(f"ngram used: {ngram}")
        documents = pickle.load(open(save_args.in_path, 'rb'))
        stop_words = get_stop_words()
        raw_corpus = get_raw_corpus(documents, stop_words)
        cook_corpus = list(get_cook_corpus(raw_corpus, ngram))
        pickle.dump(cook_corpus, open(save_args.out_path, 'wb'))
        print(f"Cook corpus saved in {save_args.out_path}")
    if save_args.artifact == 'dictionary':
        print(f"ngram used: {ngram}")
        dictionary = Dictionary(pickle.load(open(save_args.in_path, 'rb')))
        dictionary.save(save_args.out_path)
        print(f"Dictionary saved in {save_args.out_path}")
    if save_args.artifact == 'corpus':
        print(f"ngram used: {ngram}")
        documents = pickle.load(open(save_args.in_path, 'rb'))
        stop_words = get_stop_words()
        raw_corpus = get_raw_corpus(documents, stop_words)
        cook_corpus = list(get_cook_corpus(raw_corpus, ngram))
        dictionary = Dictionary(cook_corpus)
        vectorized_corpus = [dictionary.doc2bow(item) for item in cook_corpus]  # data to train.
        pickle.dump(vectorized_corpus, open(save_args.out_path, 'wb'))
        print(f"Corpus Artifact was saved under path: {save_args.out_path}")
        print(f"Dictionary Len: {dictionary.__len__()}")
    if save_args.artifact == 'model':
        vector_corpus = pickle.load(open(save_args.in_path, 'rb'))
        tfidf = TfidfModel(vector_corpus, normalize=True)  # training the model.
        tfidf.save(save_args.out_path)
        print(f"TFIDF Model was saved under path: {save_args.out_path}")
    if save_args.artifact == 'index':
        model = TfidfModel.load(save_args.in_path)
        vector_corpus = pickle.load(open(save_args.train_data, "rb"))
        index = SparseMatrixSimilarity(model[vector_corpus], num_features=int(save_args.dict_len))
        index.save(save_args.out_path)
        print(f"Sparse Matrix is saved in {save_args.out_path}")


def collect_data():
    collect_parser = argparse.ArgumentParser(
        description="Get Data from a collection."
    )
    collect_parser.add_argument("out_path", help="Path to save database")
    collect_parser.add_argument("--db_name", help="Database name to use", default=MONGO_DB)
    collect_parser.add_argument("--collection", help="Collection name", default=MONGO_COLLECTION)
    parser_args = collect_parser.parse_args(sys.argv[2:])
    collection = get_collection(parser_args.db_name, parser_args.collection)
    doc_list = list(collection.find())
    print("Loading DB into memory...")
    pickle.dump(doc_list, open(parser_args.out_path, 'wb'))
    print(f"DB({parser_args.db_name})/Collection({parser_args.collection}) is saved in {parser_args.out_path}")


def load_matrix():
    print("Loading matrix ... ")
    index = SparseMatrixSimilarity.load("index_algo.idx")
    tfidf = TfidfModel.load("model.tfidf")
    raw_corpus = pickle.load(open("corpus.raw", 'rb'))
    dictionary = Dictionary.load("dictionary_new.dict")
    db = pickle.load(open("db.db", 'rb'))
    print("Matrix Loaded ")
    return index, tfidf, raw_corpus, dictionary, db


def hc_matrix(input: str, threshold: float, index, tfidf, raw_corpus, dictionary, db, ngram=4):
    """Hardcoded similarity matrix."""
    words = get_char_ngram(input, ngram)
    items = []
    for n, s in sorted(enumerate(index[tfidf[dictionary.doc2bow(words)]]), key=lambda x: x[1], reverse=True):
        if s < float(threshold):
            break
        items.append(raw_corpus[n]['name'])

    results = [[i for i in db if j == i['normalized_name']] for j in items]
    flatten_results = [item for sublist in results for item in sublist]
    return get_product_objects(flatten_results)


def test_data():
    test_parser = argparse.ArgumentParser(
        description="Using a selected index(using a model), make querys into the model."
    )
    test_parser.add_argument("index", help="Path to index")
    test_parser.add_argument("model", help="Path to model")
    test_parser.add_argument("dictionary", help="Dictionary path")
    test_parser.add_argument("--raw_corpus", help="Raw corpus to use", default='corpus.raw')
    test_parser.add_argument("--ngram", help="NGRAM THAT IS USED IN artifacts", default=3)
    test_parser.add_argument("--db", help="DB to use", default=None)
    test_parser.add_argument("--threshold", help="Threshold min", default=0.8)
    parser_args = test_parser.parse_args(sys.argv[2:])
    index = SparseMatrixSimilarity.load(parser_args.index)
    tfidf = TfidfModel.load(parser_args.model)
    raw_corpus = pickle.load(open(parser_args.raw_corpus, 'rb'))
    dictionary = Dictionary.load(parser_args.dictionary)
    db = pickle.load(open(parser_args.db, 'rb')) if parser_args.db else None
    while True:
        inp = str(input("Texto a buscar en modelo: "))
        words = get_char_ngram(inp, int(parser_args.ngram))
        items = []
        for n, s in sorted(enumerate(index[tfidf[dictionary.doc2bow(words)]]), key=lambda x: x[1], reverse=True):
            if s < float(parser_args.threshold):
                break
            items.append(raw_corpus[n]['name'])
            print(f" Shop: {raw_corpus[n]['spider']}| Name: {raw_corpus[n]['name']}| url: {raw_corpus[n]['url']}| price: {raw_corpus[n].get('price','undefined')}| similarity:{s}")
        if db:
            results = [[i for i in db if j == i['normalized_name']] for j in items]
            flatten_results = [item for sublist in results for item in sublist]
            print("**** Final Result *****")
            for item in flatten_results:
                print(f" Shop: {item['spider']}| Name: {item['name']}| url: {item['url']}| price: {item.get('price', 'undefined')}| "
                      f"timestamp {item['timestamp']}")
            print("Productardo digamos: ", get_product_objects(flatten_results))



def get_items():
    get_parser = argparse.ArgumentParser(
        description="Get items for a spider"
    )
    get_parser.add_argument("in_path", help="Input path of a cook corpus")
    get_parser.add_argument("--spider", help='spider to use', default='adidas')
    get_parser.add_argument("--limit", help="How many items you want", default=10)
    parse_args = get_parser.parse_args(sys.argv[2:])
    raw_corpus = pickle.load(open(parse_args.in_path, 'rb'))
    # print(raw_corpus)
    raw_sp = [item for item in raw_corpus if item.get('spider', 'invalid') == parse_args.spider]
    # print(raw_sp)
    sample = [raw_sp[i] for i in sorted(random.sample(range(len(raw_sp)), int(parse_args.limit)))]
    for s in sample:
        print(f" Shop: {s['spider']}| Name: {s['name']}| url: {s['url']}| price: {s.get('price','undefined')}")


def main():
    """Save/Load documents, dictionary, corpus, etc. Accepts input to search in indexes."""
    parser = argparse.ArgumentParser(
        description='fuzzy matching command client'
    )
    parser.add_argument("action",
                        help="What action you would use?")
    args = parser.parse_args(sys.argv[1:2])
    if args.action == 'save':
        save_artifact()
    if args.action == 'collect':
        collect_data()
    if args.action == 'test':
        test_data()
    if args.action == 'random-data':
        get_items()


if __name__ == '__main__':
    main()
