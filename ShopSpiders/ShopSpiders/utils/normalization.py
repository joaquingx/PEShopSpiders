"""Normalizes text."""
import re
import unicodedata

from collections import defaultdict


def remove_non_ascii(document):
    n_word = unicodedata.normalize('NFKD', document).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return n_word


def remove_punctiation(document):
    n_word = re.sub(r'[\s]+', ' ', document)
    return n_word


def str_to_strlist(document):
    stop_list = set('a al algo es ha hay y la las lo el los o uno una un del mi soy'.split(' '))
    return [word for word in normalize(document).split() if word not in stop_list]


def normalize(document):
    return remove_punctiation(remove_non_ascii(document)).lower()


def get_frequency_for_dict(corpus):
    frequency = defaultdict(int)
    for document in corpus:
        for word in document:
            frequency[word] += 1
    return frequency
