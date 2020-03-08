"""Normalizes text."""
import re
import unicodedata


def remove_non_ascii(word):
    n_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return n_word


def remove_punctiation(word):
    n_word = re.sub(r'[\s]+', ' ', word)
    return n_word


def normalize(word):
    return remove_punctiation(remove_non_ascii(word)).lower()
