from typing import List

from data.data import get_data_file


def get_stop_words() -> List[str]:
    return open(get_data_file('stop-words.txt')).read().split(' ')


def remove_stop_words(doc: str, stop_words: List[str]) -> str:
    return ' '.join([word for word in doc.split(' ') if word not in stop_words])
