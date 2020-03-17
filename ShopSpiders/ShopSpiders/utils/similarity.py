from abc import ABC
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


def get_dictionary(corpus, f_min=1):
    non_stop_word_corpus = [str_to_strlist(document) for document in corpus]
    frequency = get_frequency_for_dict(non_stop_word_corpus)
    processed_document = [[word for word in document if frequency[word] > f_min] for document in non_stop_word_corpus]
    corpored_document = corpora.Dictionary(processed_document)
    pprint(corpored_document.token2id)
    return corpored_document


def save_model():
    corpus = [document['name'] for document in list(get_collection().find({}))]
    dictionary = get_dictionary(corpus, 1)
    bow_corpus = [dictionary.doc2bow(str_to_strlist(text)) for text in corpus]
    pprint(bow_corpus)
    tfidf = models.TfidfModel(bow_corpus)
    tfidf.save(get_data_file('tfidf_initial_model.tfidf'))
    dictionary.save_as_text(get_data_file('dictionary.dict'))
    with open(get_data_file('corpus.save'), 'w') as c_fn:
        for idx, name in enumerate(corpus):
            c_fn.write(f'{name}')
            c_fn.write('\n')


def get_local_corpus():
    corpus = list()
    with open('corpus.save', 'r') as file:
        for line in file:
            corpus.append(line.strip())
    return corpus


def load_dict_model():
    tfidf = models.TfidfModel.load(get_data_file('tfidf_initial_model.tfidf'))
    dictionary = corpora.Dictionary.load_from_text(get_data_file('dictionary.dict'))
    return dictionary, tfidf


def get_index(corpus, dictionary, model):
    bow_corpus = [dictionary.doc2bow(str_to_strlist(text)) for text in corpus]
    index = similarities.SparseMatrixSimilarity(model[bow_corpus], num_features=5000)
    return index


def similarity(corpus, sentence, dictionary, model, index):
    query_sentence = str_to_strlist(sentence)
    query_bow = dictionary.doc2bow(query_sentence)
    sims = index[model[query_bow]]
    sorted_list = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
    most_relevant = corpus[sorted_list[0][0]]
    conclusion = f"{sentence} is similar to {most_relevant} by {sorted_list[0][1]}"
    print(conclusion)
    with open('pruebas.try', 'a') as pruebas_fn:
        pruebas_fn.write(conclusion)
        pruebas_fn.write('\n')
