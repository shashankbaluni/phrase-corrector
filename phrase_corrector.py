""" module to get the correct phrase from misspled phrase """

from collections import Counter
import sys
import re
import nltk
import wordsegment as ws
import logging
import model
from preprocessor import lemmatize_tokens, remove_stop_words, tokenize, merge_tokens
import dictionary as dic

reload(sys)
sys.setdefaultencoding('utf8')

alphabet = 'abcdefghijklmnopqrstuvwxyz'

misspelled_synonym = dic.get_misspelled_synonyms()

def get_candidates(word, edits = 0):
    if edits == 1:
        return known(edits1(word))
    elif edits == 2:
        return known(edits2(word))
    else:
        return [word]


def correct(word, prev = '', nex = ''):
    """Find the best possible spelling correction for this word."""
    if prev:
        correct = word
        max_prob = 0
        for edits in range(1, 3):
            candidates = get_candidates(word, edits)
            for candidate in candidates:
                prob = cPBigram(candidate, prev)
                if prob > max_prob:
                    max_prob = prob
                    correct = candidate

            if max_prob > 0:
                break

        return [correct]
    elif nex:
        correct = word
        max_prob = 0
        for edits in range(1, 3):
            candidates = get_candidates(word, edits)
            for candidate in candidates:
                prob = cPBigram(candidate, nex=nex)
                if prob > max_prob:
                    max_prob = prob
                    correct = candidate

            if max_prob > 0:
                break

        return [correct]
    else:
        correct = word
        max_prob = 0
        for edits in range(1, 3):
            candidates = get_candidates(word, edits)
            for candidate in candidates:
                prob = fw_dictionary.get(candidate)
                if prob > max_prob:
                    max_prob = prob
                    correct = candidate

            if max_prob > 0:
                break

        return [correct]


def correct_alpha_num(word, prev = '', nex = ''):
    """Find the best spelling correction for this alphanumeric word."""
    tokens = [ token for token in re.split('(\\d+)', word) if bool(token) ]
    if len(tokens) < 3:
        corrected_tokens = []
        for i in range(len(tokens)):
            token = tokens[i]
            if token and not token.isdigit() and i == 0:
                tokens[i] = correct(token, prev=prev, nex=tokens[1])[0]
                corrected_tokens.append(tokens[i])
            elif token and not token.isdigit() and i == 1:
                tokens[i] = correct(token, prev=tokens[0], nex=nex)[0]
                corrected_tokens.append(tokens[i])
            elif token.isdigit() and len(token) < 5:
                if i > 0 and cPBigram(token, tokens[i - 1]) > 0:
                    corrected_tokens.append(token)
                elif i > 0:
                    corrected_tokens.append(correct(token, prev=tokens[0])[0])
                elif i == 0 and dictionary[tokens[i]] > 1:
                    corrected_tokens.append(correct(tokens[i], nex=tokens[1])[0])
                elif i == 0 and dictionary[tokens[i]] < 1:
                    corrected_tokens.append(token)
            else:
                corrected_tokens.append(tokens[i])

        return corrected_tokens
    else:
        return [word]


def known(words):
    """Return the subset of words that are actually in the dictionary."""
    return {w for w in words if w in dictionary}


def edits0(word):
    """Return all strings that are zero edits away from word (i.e., just word itself)."""
    return {word}


def edits1(word):
    """Return all strings that are one edit away from this word."""
    pairs = splits(word)
    deletes = [ a + b[1:] for a, b in pairs if b ]
    transposes = [ a + b[1] + b[0] + b[2:] for a, b in pairs if len(b) > 1 ]
    replaces = [ a + c + b[1:] for a, b in pairs for c in alphabet if b ]
    inserts = [ a + c + b for a, b in pairs for c in alphabet ]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    """Return all strings that are two edits away from this word."""
    return {e2 for e1 in edits1(word) for e2 in edits1(e1)}


def splits(text, start = 0, L = 20):
    """Return a list of all (first, rest) pairs; start <= len(first) <= L."""
    return [ (text[:i], text[i:]) for i in range(start, min(len(text), L) + 1) ]


def pdist(counter, total):
    """Make a probability distribution, given evidence from a Counter."""
    return lambda x: counter[x] / total


def Pwords(words):
    """Probability of words, assuming each word is independent of others."""
    return product((P1w(w) for w in words))


def product(nums):
    """Multiply the numbers together.  (Like `sum`, but with multiplication.)"""
    result = 1
    for x in nums:
        result *= x

    return result


def Pwords2(words, prev = '<S>'):
    """The probability of a sequence of words, using bigram data, given prev word."""
    return product((cPword(w, prev if i == 0 else words[i - 1]) for i, w in enumerate(words)))


def cPword(word, prev):
    """Conditional probability of word, given previous word."""
    bigram = prev + ' ' + word
    if P2w(bigram) > 0 and P1w(prev) > 0:
        return P2w(bigram) / P1w(prev)
    else:
        return P1w(word) / 2


def cPBigram(word, prev='', nex=''):
    """Conditional probability of bigarm only else 0, given previous word."""

    if prev:
        bigram = prev + ' ' + word
    elif nex:
        bigram = word + ' ' + nex
    else:
        return 0

    if prev and P2w(bigram) > 0 and P1w(prev) > 0:
        return P2w(bigram) / P1w(prev)
    elif nex and P2w(bigram) > 0 and P1w(nex) > 0: 
        return P2w(bigram) / P1w(nex)
    else:
        return 0


def segment2(text, prev = '<S>'):
    """Return best segmentation of text; use bigram data."""
    if not text:
        return []
    else:
        candidates = ([first] + segment2(rest, first) for first, rest in splits(text, 1))
        return max(candidates, key=lambda words: Pwords2(words, prev))


def cleanQuery(query):
    
    tokens = tokenize(query)
    query = []
    for i in range(len(tokens)):
        token = tokens[i]
        print('token : ', token)
        
        if not bool(re.search('^\d+$', token)):
            alpha_num = bool(re.search('(^\d+|\d+$)', token))
            if misspelled_synonym.has_key(token):
                print('i am here 1')
                token = misspelled_synonym[token]
                query = query + tokenize(token)
                continue
            elif i == 0 and len(tokens) == 1 and dictionary[token] < 50 and alpha_num:
                print('i am here 2')
                token = correct_alpha_num(token)
            elif i == 0 and len(tokens) == 1 and fw_dictionary[token] < 50:
                print('i am here 3')
                token = correct(token)
            elif i == 0 and len(tokens) > 1 and dictionary[tokens[1]] > 50 and alpha_num:
                print('i am here 4')
                token = correct_alpha_num(token, nex=tokens[1])
            elif i == 0 and len(tokens) > 1 and dictionary[token] < 450 and dictionary[tokens[1]] < 20:
                print('i am here 5')
                token = correct(token)
            elif i == 0 and len(tokens) > 1 and dictionary[tokens[1]] > 50 and cPBigram(word=token, nex=tokens[1]) == 0:
                print('i am here 6')
                token = correct(token, nex=tokens[1])
            elif i > 0 and dictionary[query[-1]] >= 1 and cPBigram(word=token, prev=query[-1]) == 0 and alpha_num:
                print('i am here 7')
                token = correct_alpha_num(token, prev=query[-1])
            elif i > 0 and dictionary[query[-1]] >= 20 and cPBigram(token, query[-1]) == 0:
                print('i am here 8' + query[-1])
                token = correct(token, prev=query[-1])
            elif i > 0 and dictionary[token] <= 5 and cPBigram(token, query[-1]) == 0:
                print('i am here 9')
                token = correct(token)
            else:
                print('i am here 10')
                query.append(token)
                continue

            for tkn in token:
                if dictionary[tkn]:
                    query.append(tkn)
                elif len(tkn) <= 15:
                    sep_tokens = ws.segment(tkn)
                    if Pwords2(sep_tokens) >= 1.5e-06:
                        query = query + sep_tokens
                    else:
                        query.append(tkn)
                else:
                    query.append(tkn)

        else:
            query.append(token)

    clean_query = []
    for token in merge_tokens(query):
        clean_query = clean_query + tokenize(misspelled_synonym.get(token, token))

    return (' '.join(clean_query), Pwords2(clean_query))

dictionary, fw_dictionary, bigram_dictionary = dic.get_dictionaries()

print 'dictionary size : ', len(dictionary)
print 'first word dictionary size : ', len(fw_dictionary)
print 'bigram dictionary size : ', len(bigram_dictionary)

max_word_length = max(map(len, dictionary))
P1w = pdist(dictionary, float(sum(dictionary.values())))
P2w = pdist(bigram_dictionary, float(sum(bigram_dictionary.values())))