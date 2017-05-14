""" module for saving and loading dictionaries """
import os
import pickle

FILE_DIR = os.path.dirname(os.path.realpath('__file__'))

def save_dictionary(filename, obj):
    """save the dictionary into a file"""
    filename = os.path.join(FILE_DIR, 'assets/obj/' + filename)
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_dictionary(filename):
    """load dictionary from the file"""
    filename = os.path.join(FILE_DIR, 'assets/obj/' + filename)
    try:
        with open(filename, 'rb') as input:
            return pickle.load(input)
    except Exception as e:
        print("exception", e)