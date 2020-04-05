import argparse, utils, sys, readline
from scipy.spatial.distance import cosine
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import nltk
from nltk.corpus import stopwords
from stop_words import get_stop_words


stopword = set(stopwords.words('english'))
additional = {"$mention$", "could" , "would", "should", "the", "and", "so", "certainly", "shouldn't",\
"books", "likely", "agree", "thanks", "folks", "gegen", "first", "however", "summary", "chose", "verdad" \
"maybe", "everything", "around", "thing", "name", "seems"}
stopword.update(additional)
# stopword = get_stop_words("english")

class autovivify_list(dict):
  '''A pickleable version of collections.defaultdict'''
  def __missing__(self, key):
    '''Given a missing key, set initial value to an empty list'''
    value = self[key] = []
    return value

  def __add__(self, x):
    '''Override addition for numeric types when self is empty'''
    if not self and isinstance(x, Number):
      return x
    raise ValueError

  def __sub__(self, x):
    '''Also provide subtraction method'''
    if not self and isinstance(x, Number):
      return -1 * x
    raise ValueError


def word_arithmetic(start_word, minus_words, plus_words, word_to_id, id_to_word, df, num_results=5):
    '''Returns a word string that is the result of the vector arithmetic'''
    try:
        start_vec  = df[word_to_id[start_word]]
        minus_vecs = [df[word_to_id[minus_word]] for minus_word in minus_words]
        plus_vecs  = [df[word_to_id[plus_word]] for plus_word in plus_words]
    except KeyError as err:
        return err, None


    result = start_vec

    if minus_vecs:
        for i, vec in enumerate(minus_vecs):
            result = result - vec

    if plus_vecs:
        for i, vec in enumerate(plus_vecs):
            result = result + vec

    # result = start_vec - minus_vec + plus_vec
    words = [start_word] + minus_words + plus_words
    return None, find_nearest(words, result, id_to_word, df, num_results)

def find_nearest(words, vec, id_to_word, df, num_results, method='cosine'):

    if method == 'cosine':
        minim = [] # min, index
        for i, v in enumerate(df):
            # skip the base word, its usually the closest
            if id_to_word[i] in words:
                continue
            if len(id_to_word[i]) < 4:
                continue
            dist = cosine(vec, v)
            minim.append((dist, i, v))
        minim = sorted(minim, key=lambda v: v[0])
        # return list of (word, cosine distance) tuples
        return [(id_to_word[minim[i][1]], minim[i][0], minim[i][2]) for i in range(num_results)]
    else:
        raise Exception('{} is not an excepted method parameter'.format(method))

def parse_expression(expr):

    # split = expr.split()
    # start_word = split[0]
    # minus_words, plus_words = [], []
    # for i, token in enumerate(split[1:]):
    #     if token == '+':
    #         plus_words.append(split[i + 2])
    #     elif token == '-':
    #         minus_words.append(split[i + 2])
    word = expr
    # return start_word, minus_words, plus_words
    return word

def display_closestwords_tsnescatterplot(word, results):

    # arr = np.empty((0,300), dtype='f')
    # word_labels = [word]

    # # get close words
    # close_words = model.similar_by_word(word)

    # # add the vector for each of the closest words to the array
    # arr = np.append(arr, np.array([model[word]]), axis=0)
    # for wrd_score in close_words:
    #     wrd_vector = model[wrd_score[0]]
    #     word_labels.append(wrd_score[0])
    #     arr = np.append(arr, np.array([wrd_vector]), axis=0)

    # find tsne coords for 2 dimensions
    word_labels = [word]
    for res in results:
        word_labels.append(res[0])

    arr = np.empty((1,50))

    for res in results:

        arr = np.concatenate((arr, np.reshape(res[2], (1, 50))), axis = 0)

    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(arr)

    x_coords = Y[:, 0]
    # print(x_coords)
    y_coords = Y[:, 1]
    # display scatter plot
    plt.scatter(x_coords, y_coords)

    for label, x, y in zip(word_labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.xlim(x_coords.min()+0.00005, x_coords.max()+0.00005)
    plt.ylim(y_coords.min()+0.00005, y_coords.max()+0.00005)
    #plt.show()

    file_name = word + "Closest.png"
    plt.savefig(file_name)
    return



def find_word_clusters(labels_array, cluster_labels):
  '''Return the set of words in each cluster'''
  cluster_to_words = autovivify_list()
  for c, i in enumerate(cluster_labels):
    cluster_to_words[ i ].append( labels_array[c] )
  return cluster_to_words


def process(num_results, start_word):
    #inpt = input('> ')
    #if inpt == 'exit':
    #    print("EXITING")
    #    exit()
    # start_word = parse_expression(inpt)

    # err, results = word_arithmetic(start_word=start_word,
    #                               minus_words=minus_words,
    #                               plus_words=plus_words,
    #                               word_to_id=word_to_id,
    #                               id_to_word=id_to_word,
    #                               df=df,
    #                               num_results=num_results)

    results = find_nearest(start_word, df[word_to_id[start_word]], id_to_word, df, num_results, method='cosine')



    print("CLOSEST WORDS: ")
    if results:
        print()
        for res in results:
            print(res[0].ljust(15), '     {0:.2f}'.format(res[1]))
        print()
    else:
        print('{} not found in the dataset.'.format(err), file=sys.stderr)

    display_closestwords_tsnescatterplot(start_word, results)

# Start the process of discovering keywords via cosine distance
def discover_keywords(start_word, num_words):
    process(num_words, start_word)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vector_dim', '-d',
                        type=int,
                        choices=[50, 100, 200, 300],
                        default=100,
                        help='What vector GloVe vector depth to use '
                             '(default: 100).')
    parser.add_argument('--num_words', '-n',
                        type=int,
                        default=10000,
                        help='The number of lines to read from the GloVe '
                             'vector file (default: 10000).')
    parser.add_argument('--num_output', '-o',
                        type=int,
                        default=1,
                        help='The number of result words to display (default: 1)')
    parser.add_argument('--glove_path', '-i',
                        default='data/glove',
                        help='GloVe vector file path (default: data/glove)')
    return parser.parse_args()



# takes input of the form python word_dist.py key_word
if __name__ == '__main__':

    keyword = input('Starting word: ')
    num_words = input('Number of keywords: ')
    #args = parse_args()
    vector_file = 'GloVe-1.2/vectors.txt'

    num_lines = 0
    with open(vector_file, 'r') as f:
        for line in f:
            num_lines += 1
    #if args.num_words > 400000:
    #    print('--num_words must be equal to or less than 400,000. Exiting.')
    #    exit(1)

    df, labels_array = utils.build_word_vector_matrix(vector_file, num_lines)
    word_to_id, id_to_word = utils.get_label_dictionaries(labels_array)


    # Processing the num_output parameter to visualize 15 closest words FIRST
    #keyword = sys.argv[-1]
    discover_keywords(keyword, int(num_words))
    discover = True
    while discover == True:
        keyword = input('Starting word: ')
        num_words = input('Number of keywords: ')
        if keyword == "quit":
            discovered = False
            break
        discover_keywords(keyword, int(num_words))
        

    # k-means clustering with 100 clusters
    kmeans_model = KMeans(init='k-means++', n_clusters=100, n_init=10)
    kmeans_model.fit(df)

    cluster_labels  = kmeans_model.labels_
    cluster_inertia   = kmeans_model.inertia_
    cluster_to_words  = find_word_clusters(labels_array, cluster_labels)


    count = 0
    arr = np.empty((1,50))
    word_labels = []
    num = []
    for c in cluster_to_words:
        print(cluster_to_words[c])
        print("\n")
        if "hillary" in cluster_to_words[c] or "trump" in cluster_to_words[c]:
            j = 0
            for word in cluster_to_words[c]:
                if word.lower() not in stopword and len(word) > 4:
                    word_labels.append(word.lower())
                    print("Appending: " + word.lower())
                    arr =  np.concatenate((arr, np.reshape(df[word_to_id[word]], (1, 50))), axis = 0)
                    j = j+1
                #print(arr)
            print(j)
            num.append(j)
    # Performing dimensionality reduction to visualize the words in the clusters
    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    print(arr)
    Y = tsne.fit_transform(arr)

    x_coords = Y[:, 0]
    # print(x_coords)
    y_coords = Y[:, 1]


    print(num)
    print(np.shape(x_coords))
    # Visualizing Kavannaugh and Epstein clusters (i.e. the 15 words closest to them)
    plt.scatter(x_coords[0:15], y_coords[0:15], c = "r")
    plt.scatter(x_coords[num[0]:num[0]+15], y_coords[num[0]:num[0]+15], c = "b")

    group_1 = []
    group_2 = []

    for label, x, y in zip(word_labels[0:15], x_coords[0:15], y_coords[0:15]):
        group_1.append(label)
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points', fontsize=12, rotation=-20)

    for label, x, y in zip(word_labels[num[0]:num[0]+15], x_coords[num[0]:num[0]+15], y_coords[num[0]:num[0]+15]):
        group_2.append(label)
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points',fontsize=12, rotation=-10)

    plt.xlim(x_coords.min()+0.00005, x_coords.max()+0.00005)
    plt.ylim(y_coords.min()+0.00005, y_coords.max()+0.00005)
    #plt.axis('off')
    print("Subtopic 1: " + str(group_1))
    print("Subtopic 2: " + str(group_2))
    #plt.show()
    #process(args.num_output)
    #while True:
         #process(args.num_output)
