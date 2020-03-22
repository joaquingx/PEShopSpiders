"""PAUSED: Machine learning implementation for similarities."""
from collections import defaultdict
from pprint import pprint
from gensim import corpora, models, similarities
from gensim.interfaces import SimilarityABC, TransformationABC
from typing import Type, List
from utils.normalization import normalize, get_frequency_for_dict, str_to_strlist
from utils.mongo_db_utils import get_collection
from data import get_data_file


class FeatureVector:
    """Receives a document and transforms it to feature vector."""


class Comparator:
    corpus = None
    similarity: Type[SimilarityABC]

    def __init__(self, corpus: List[FeatureVector], similarity: Type[SimilarityABC]):
        self.model = corpus
        self.similarity = similarity

    def _get_comparator(self):
        self.comparator = self.similarity(corpus=self.corpus)

    def query(self, f_vector: FeatureVector) -> (str, float):
        result = self.comparator[f_vector]
        sorted_list = sorted(enumerate(result), key=lambda x: x[1], reverse=True)
        return sorted_list[0][0], sorted_list[0][1]


class Model:
    model_type: Type[TransformationABC]

    def __init__(self, model_type, bow):
        self.model_type = model_type
        self.trained_model = self.model_type(bow)

    @classmethod
    def load_model(cls, model, path):
        cls.model_type = model
        cls.trained_model = cls.model_type.load(path)

    def save(self, filename):
        self.trained_model.save(get_data_file(filename))


#TODO DEFINE BETTER CORPUS IS TOO AMBOIGOUS
class CorpusCleaner:
    """Clean a corpus."""
    def clean_corpus(self, corpus: List[str], f_min=1):
        str_lists = self.list_to_str_lists(corpus)
        cleaned = self.remove_trivial_words(self.remove_stop_words(str_lists), f_min)
        return cleaned

    @staticmethod
    def list_to_str_lists(str_lists):
        return [[word for word in normalize(document).split()] for document in str_lists]

    @staticmethod
    def remove_stop_words(str_lists):
        stop_list = set('a al algo es ha hay y la las lo el los o uno una un del mi soy'.split(' '))
        return [[word for word in document if word not in stop_list] for document in str_lists]

    @staticmethod
    def _get_frequency(str_lists):
        frequency = defaultdict(int)
        for document in str_lists:
            for word in document:
                frequency[word] += 1
        return frequency

    def remove_trivial_words(self, str_lists, f_min):
        frequency = self._get_frequency(str_lists)
        return [[word for word in document if frequency[word] > f_min] for document in str_lists]


class Dictionary:
    corpus: List[str] = None
    dictionary: corpora.Dictionary
    cleaner = CorpusCleaner()

    def __init__(self, doc_list):
        self.doc_list = doc_list
        cleaned_document = self.cleaner.clean_corpus(self.doc_list)
        self.dictionary = corpora.Dictionary(cleaned_document)

    def save(self, filename):
        self.dictionary.save_as_text(get_data_file(filename))