python similarity.py save corpus texto.txt corpus_trigram.txt --ngram=$1; python similarity.py save model corpus_trigram.txt model.tfidf; python similarity.py save cook_corpus texto.txt cook.new --ngram=$1; python similarity.py save dictionary cook.new dictionary_new.dict --ngram=$1; python similarity.py save raw_corpus texto.txt corpus.raw;  python similarity.py save index model.tfidf index_new.idx --train_data=corpus_trigram.txt