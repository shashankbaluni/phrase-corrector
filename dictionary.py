""" Load all the dictionaries"""

from collections import Counter
import nltk
import model
from preprocessor import lemmatize_tokens, remove_stop_words, tokenize, merge_tokens

def get_misspelled_synonyms():

    SYNONYMS_DICTIONARY = 'synonyms'
    synonyms_dic = model.load_dictionary(SYNONYMS_DICTIONARY)

    if not synonyms_dic:
        text = open('assets/csv/synonym.txt').read()
        synonyms_dic = {}
        rows = text.split('\n')
        for row in rows:
            row = row.split('=>')
            if len(row) > 1:
                word = row[1].strip()
                synonyms = row[0].split(',')
                for synonym in synonyms:
                    synonyms_dic[synonym.strip()] = word
        model.save_dictionary(SYNONYMS_DICTIONARY, synonyms_dic)

    return synonyms_dic

def get_dictionaries():
    """ function to load all the dictionaries into the memory"""
    queries = unicode(open('assets/csv/clean_query.txt').read(), 'utf-8').split('\n')
    dictionary_fw = []
    total_bigram = []
    dictionary_name = 'dictionary'
    fw_dictionary_name = 'fw_dictionary'
    bigram_dictionary_name = 'bigram_dictionary'

    dictionary = model.load_dictionary(dictionary_name)
    fw_dictionary = model.load_dictionary(fw_dictionary_name)
    bigram_dictionary = model.load_dictionary(bigram_dictionary_name)

    if not (dictionary and fw_dictionary and bigram_dictionary):

        for query in queries:
            tokens = tokenize(query)
            dictionary_fw.append(tokens[0])
            dictionary_fw.append(lemmatize_tokens(tokens[0])[0])
            query_bigram = list(nltk.bigrams(tokens)) + list(nltk.bigrams(remove_stop_words(tokens))) + list(nltk.bigrams(lemmatize_tokens(tokens))) + list(nltk.bigrams(lemmatize_tokens(remove_stop_words(tokens))))
            for bigram in query_bigram:
                total_bigram.append(' '.join(bigram))

        all_tokens = tokenize(' '.join(queries))
        dictionary = Counter(all_tokens) + Counter(lemmatize_tokens(all_tokens))
        fw_dictionary = Counter(dictionary_fw)
        bigram_dictionary = Counter(total_bigram)

        for key in dictionary.keys():
            if dictionary[key] < 5:
                del dictionary[key]
        for key in bigram_dictionary.keys():
            if bigram_dictionary[key] < 2:
                del bigram_dictionary[key]

        model.save_dictionary(dictionary_name, dictionary)
        model.save_dictionary(fw_dictionary_name, fw_dictionary)
        model.save_dictionary(bigram_dictionary_name, bigram_dictionary)
    return dictionary, fw_dictionary, bigram_dictionary
    
