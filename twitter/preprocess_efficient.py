__author__ = "Maya"
__version__ = 1.0
'''Preprocessing script for social media data that uses parallel processing with dask.
Warning: no lemmatization, as not doing so gives better results for dynamic
keyword search. '''

import preprocessor as p
import re

import sys

# remove stopwords
import nltk
from nltk.corpus import stopwords

from nltk.corpus import sentiwordnet as swn
# Do this first, that'll do something eval()
# to "materialize" the LazyCorpusLoader
#next(swn.all_senti_synsets()) # This is most likely considerably more inefficient...

#nltk.download('stopwords')
#import spacy
#nlp = spacy.load("en_core_web_sm")

import dask.dataframe as dd
import pandas as pd

# from stop_words import get_stop_words
# stemming
from nltk.stem import PorterStemmer
# lemmatization
from nltk.stem import WordNetLemmatizer
import string

# Initializing lemmatization object
#lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
import time
import string

p.set_options(p.OPT.EMOJI, p.OPT.SMILEY) #, p.OPT.URL)


# Storing stopwords
punctuation = list(string.punctuation)
stop_words = stopwords.words('english')
stop_words.append("amp")

def check_ascii(line):
    if line is not None:
        temp = line.encode('ascii', 'ignore')
        try:
            temp.decode('ascii')
            return line
        except UnicodeDecodeError:
            return ''
    return ''

# Using tweet-preprocessor's clean function to remove urls
# and emojis.
def cleanLine(line):
    """returns line with urls, mentions, and emojis removed. """
    if line is not None:
        return p.clean(line)
    else:
        return ''

def regexchars(line):
    """ Returns string with alphabetical characters,
    basic puncation, or hashtags sign only. (no numbers)"""
    # remove URLS (second layer)
    res = re.sub(r"http\S+", " ", line) # removing URLs with http
    res1 = re.sub(r"https\S+", " ", res) # removing URLs with https
     # keeping mentions, hashtags intact
    return re.sub(r"[^a-zA-Z\#\@]", " ", res1).lower()


# Tokenize
def tokenize(line):
    """ Returns a list of tokens. """
    tokens = p.tokenize(line)
    print(tokens)
    return tokens.split()

# Filtering function to remove stopwords from a line
def removeStopwords(words):
    """ Takes as input a list returned from tokenize and
    returns a list of non-stop-words in teh line. """

    filtered = filter(lambda word: word not in stop_words, words)
    filtered2 = filter(lambda word: len(word) > 2, filtered)
    #return list(filtered2)

    return " ".join(filtered2)

# def lemmatize_stem(words):
#     """ Takes as input a list of words from "removeStopwords and
#     lemmatizes each word, joins them, and returns them as the final
#     preprocessed string. """
#     lemmatizer = WordNetLemmatizer()
#     lemmatized_words = [lemmatizer.lemmatize(x) for x in words]
#     #stemmed_words = [stemmer.stem(x) for x in words]
#     res = " ".join(lemmatized_words)
#     #print(res)
#     return res

# def lemmatize(text, nlp=nlp):
#
#     doc = nlp(" ".join(text))
#
#     lemmatized = [token.lemma_ for token in doc]
#     print(lemmatized)
#     return lemmatized

def applyfunctions(df):
    ls = df.tweets.map(check_ascii).map(cleanLine).map(regexchars).map(tokenize).\
    map(removeStopwords)
    return pd.DataFrame(ls)

def preprocess(inFile, outputFile):

    start = time.time()
    print("entered preprocess....")
    # Load in csv, 1 partition per cpu
    df = pd.read_csv(inFile, engine='python')

    #df.columns = ['reply_text', 'vader']
    #df = df[['reply_text']]
    df = df[['tweets']]

    dask_dataframe = dd.from_pandas(df, npartitions=6)
    #df = applyfunctions(df)
    # Map functions to each partition
    result = dask_dataframe.map_partitions(applyfunctions, meta=df)
    print("mapped partitions...")
    df = result.compute()

    # Write resulting dataframe to csv file
    df.to_csv(outputFile, header=None, index=False)
    end = time.time()
    print("length of dataset: ", len(df.tweets))
    print("Preprocessing complete, time taken: ", (end-start))


if __name__ == '__main__':

     inFile = input('Name of input file?: ')
     outputFile = input('Name of output file? : ')
     print("\n\nSTART...")
     preprocess(inFile, outputFile)
     #parseFile(inFile, outputFile)
