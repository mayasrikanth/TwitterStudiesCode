"""
Minimal Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""

import os

from os import path
from wordcloud import WordCloud
import csv

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# # Read the whole text.
# text = open(path.join(d, 'constitution.txt')).read()

# Generate a word cloud image
# where is text cloud being updated? (manually)
reader = csv.reader(open('text_cloud', 'r',newline='\n'))
d = {}
for k,v in reader:
    d[k] = int(1.0/float(v))
    print(d[k])

#Generating wordcloud. Relative scaling value is to adjust the importance of a frequency word.
#See documentation: https://github.com/amueller/word_cloud/blob/master/wordcloud/wordcloud.py
wordcloud = WordCloud(width=900,height=500, background_color = "white", normalize_plurals=False).generate_from_frequencies(d)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
# lower max_font_size
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()
