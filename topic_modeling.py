""" module to topic modeling the provided strings """
import os
import logging
import preprocessor
from gensim import corpora, models, similarities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

QUERIES = unicode(open('assets/csv/clean_query.txt').read(), 'utf-8').split('\n')
QUERIES = list(set(QUERIES))

if os.path.exists("./assets/obj/deerwester.dict"):
    DICTIONARY = corpora.Dictionary.load('./assets/obj/deerwester.dict')
else:
    TEXTS = []
    for query in QUERIES:
        stopwords_removed = preprocessor.remove_stop_words(preprocessor.tokenize(query))
        TEXTS.append(preprocessor.lemmatize_tokens(stopwords_removed))

    DICTIONARY = corpora.Dictionary(texts)
    DICTIONARY.filter_extremes(no_below=10)
    DICTIONARY.save('./assets/obj/deerwester.dict')

if os.path.exists("./assets/obj/deerwester.mm"):
    CORPUS = corpora.MmCorpus('./assets/obj/deerwester.mm')
else:
    CORPUS = [DICTIONARY.doc2bow(text) for text in TEXTS]
    corpora.MmCorpus.serialize('./assets/obj/deerwester.mm', CORPUS)

# if (os.path.exists("./assets/obj/model.lsi")):
# 	lsi = models.LsiModel.load('./assets/obj/model.lsi')
# else:
# 	tfidf = models.TfidfModel(corpus)
# 	corpus_tfidf = tfidf[corpus]
# 	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=500)
# 	corpus_lsi = lsi[corpus_tfidf]
# 	lsi.save('./assets/obj/model.lsi')

if os.path.exists("./assets/obj/model_corpus.lsi"):
    LSI = models.LsiModel.load('./assets/obj/model_corpus.lsi')
else:
    LSI = models.LsiModel(CORPUS, id2word=DICTIONARY, num_topics=500)
    LSI.save('./assets/obj/model_corpus.lsi')


if os.path.exists("./assets/obj/deerwester.index"):
    INDEX = similarities.MatrixSimilarity.load('./assets/obj/deerwester.index')
else:
    INDEX = similarities.MatrixSimilarity(lsi[corpus], num_features=500)
    INDEX.save('./assets/obj/deerwester.index')

def get_similar_queries(query):
    """ find all the similar topics of the provided query"""
    vec_bow = DICTIONARY.doc2bow(preprocessor.lemmatize_tokens(preprocessor.remove_stop_words(preprocessor.tokenize(query))))
    sims = INDEX[LSI[vec_bow]]

    similar_queries = []
    i = 1
    for document_number in sorted(enumerate(sims), key=lambda item: -item[1]):
        similar_queries.append(queries[document_number])
        if i >= 5:
            break
        i += 1

    return similar_queries
