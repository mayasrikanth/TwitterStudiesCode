import preprocessor as p
import re
# remove stopwords
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
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
stop_words = stopwords.words('english') + punctuation + ["MENTION"]
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
def parseFile(filename):
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
                    # remove stopwords from line before tokenizing
                    #print(row[0])
                    tokens = p.tokenize(row[0])
                    #tokens = word_tokenize(row[0])
                    #tokens = [i for i in tokens if i not in stop_words]
                    letters_only_text = re.sub("^[a-z A-Z]", "", tokens)
                    word_array = letters_only_text.split()
                    word_array = [term for term in word_array if term not in stop_words]
                    # Stemming (TOO STRONG...)
                    #word_array = map(stem, word_array)
                    # Recreating string
                    cleaned = " ".join(word_array)
                    print(cleaned)
                    preprocessed.append(cleaned)
                    line_count += 1
        print(f'Processed {line_count} lines.')
    print(len(preprocessed))

# Calling parse file function now with two files
parseFile('TweetText30Day.txt') # Collecting late-september from sandbox
parseFile('MeTooRound2.txt') # Collecting late-august from standard search
parseFile('MeTooTweetsOct.txt') # Collected mid-october from standard search

# Combining various data
with open('camReadyResults.csv', mode='a') as csv_file:
    for i in range(len(preprocessed)):
           csv_file.write(preprocessed[i])
           csv_file.write('\n')
           csv_file.write('\n')


#with open('preprocessd_SandboxOld.csv', mode='w') as csv_file:
    
  #  for i in range(len(preprocessed)):

    #    csv_file.write(preprocessed[i])
     #   csv_file.write('\n')
      #  csv_file.write('\n')
