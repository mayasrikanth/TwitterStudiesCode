import preprocessor as p
import re

import sys


# remove stopwords
import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')

# from stop_words import get_stop_words
# stemming
from nltk.stem import PorterStemmer
# lemmatization
from nltk.stem import WordNetLemmatizer
import string
import csv


p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.EMOJI, p.OPT.SMILEY)
preprocessed = []

# Storing stopwords
punctuation = list(string.punctuation)
stop_words = stopwords.words('english')

def deEmojify(inputString):
    temp = inputString.encode('ascii', 'ignore')
    try:
        temp.decode('ascii')
    except UnicodeDecodeError:
        print("it was not a ascii-encoded unicode string")
    else:
        print("we good")
        return temp.decode('ascii')
    #return inputString.encode('ascii', 'ignore').decode('ascii')

# Initializing stemming and lemmatization objects
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
# Filtering function to remove stopwords from a line
def removeStopWords(w):
    if (w in stop_words):
        return False
    else:
        return True

# Stemming function
def stem(w):
    return stemmer.stem(w)


def parseFile(filename, outfile):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\n')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #print(row)
                print(line_count)
                if len(row) is not 0:
                    print(row)
                    if line_count == 689835:
                        print("here's the problematic row: ", row)
                    # Removing mentions, URLS, emojiis and tokenizing
                    clean_row = p.clean(row[0])
                    clean_row = deEmojify(clean_row)
                    tokens = p.tokenize(clean_row)




                    temp = " {}"
                    final = temp.format(tokens)

                    letters_only_text = re.sub(r"[^a-zA-Z\'\#]", " ", final).lower()
                    word_array = letters_only_text.split()
                    word_array = [term for term in word_array if term not in stop_words]

                    # Recreating string
                    cleaned = " ".join(word_array)
                    print(cleaned)
                    if len(cleaned) > 0:
                        preprocessed.append(cleaned)
                    line_count += 1

        print(f'Processed {line_count} lines.')
    print(len(preprocessed))

    # Writing preprocessed, emoji-free tweets to csv file.
    with open(outfile, mode='w') as csv_file:
        for i in range(len(preprocessed)):
               csv_file.write(preprocessed[i])
               csv_file.write('\n')
               csv_file.write('\n')

# takes input of form: python3 preprocess.py inputfile.json outputfile.txt
if __name__ == '__main__':

     inFile = input('Name of input file?: ')
     outputFile = input('Name of output file? : ')
     #inFile = sys.argv[-2] #(2nd to last arg on command line)
     #outputFile = sys.argv[-1]
     parseFile(inFile, outputFile)
