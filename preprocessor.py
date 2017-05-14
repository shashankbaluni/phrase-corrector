""" preprocess the queries """

import sys
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import MWETokenizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import model

reload(sys)
sys.setdefaultencoding('utf8')

STOP_WORDS = set(stopwords.words('english'))
MERGE_TOKENS = [('blue', 'tooth'),
                ('i', 'ball'),
                ('i', 'phone'),
                ('fit', 'bit'),
                ('t', 'shirt'),
                ('i', 'pod'),
                ('t', 'shirts'),
                ('men', "'s"),
                ('mac', 'book'),
                ('women', "'s"),
                ('pen', 'drive'),
                ('pan', 'drive'),
                ('red', 'mi'),
                ('cash', 'back'),
                ('by', 'cycle'),
                ('bi', 'cycle'),
                ('fast', 'rack'),
                ('wo', 'men'),
                ('fast', 'track'),
                ('wood', 'land'),
                ('micro', 'wave'),
                ('ear', 'phone'),
                ('anti', 'virus'),
                ('promo', 'code'),
                ('back', 'pack'),
                ('wi', 'fi'),
                ('key', 'board'),
                ('levi', "'s"),
                ("l'", 'oreal'),
                ('f', 'and', 'd'),
                ('f', 'n', 'd')]


tokenizer = RegexpTokenizer(r'\-|\s+|\+|[\(\)]|\'\'|"', gaps=True)
mweTokenizer = MWETokenizer(MERGE_TOKENS, separator='')
wordnet_lemmatizer = WordNetLemmatizer()

def tokenize(query):
    """ tokenize query """
    query = query.lower()
    query = tokenizer.tokenize(query)
    return query


def lemmatize_tokens(tokens):
    """ lemmatize provided tokens """
    return [wordnet_lemmatizer.lemmatize(token) for token in tokens]


def merge_tokens(tokens):
    """ merge tokens """
    return mweTokenizer.tokenize(tokens)


def remove_stop_words(tokens):
    """ remove stop words from tokens """
    return [token for token in tokens if token not in STOP_WORDS]
    