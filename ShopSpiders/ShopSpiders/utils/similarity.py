from pprint import pprint
from gensim import corpora, models, similarities

from utils.normalization import str_to_strlist, get_frequency_for_dict
from utils.mongo_db_utils import get_collection
from data import get_data_file


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
