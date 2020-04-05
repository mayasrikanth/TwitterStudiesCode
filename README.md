# TwitterStudiesCode

# Motivation 

Code for an ongoing project to understand network effects 
and sentiment propogation in a social media network, with 
the ultimate aim of reducing online abuse using AI techniques. 
The current focusof the project is the #MeToo twitter movement--all Twitter
data analyzed thus far is queried on a #MeToo-related keyword. 

Collaborators: 
- Maya Srikanth
- Angie Liu 
- Nicholas Adams-Cohen
- Dr. R. Mike Alvarez
- Dr. Anima Anandkumar


## Recent Work 
See https://arxiv.org/abs/1911.05332 to read more about our ongoing work where we use
natural language proceessing techniques to uncover keywords in social media 
data for troll detection. Our keyword extraction methods currently utilize GloVe (Global Vectors for 
Word Representation), a renown word embedding model proposed in 2014 by Stanford Researchers.
See the explanation of the model here: https://nlp.stanford.edu/projects/glove/.


# What is this code for?

This repository contains code to preprocess your social media data, construct GloVe representation of 
all non "stop words" in your corpus, produce meaningful visualizations of keywords or hashtags, and
expose conversation topics in your data using cluster analysis (specifically, k-means clustering).

As this is an ongoing project, I am working to include additional scripts for topic modeling analysis using 
LDA.

## Required External Libraries
- nltk 
- word cloud 
- pandas 

## File Organization 


## Commands 

### PREPROCESSING DATA

To preprocess your data, drag your .csv file into the "twitter" directory. In your
terminal, run the following command. You will be prompted to enter the name of your raw data, as well as the name of your preprocessed output file. 

```linux
python preprocess.py
```

### Training GLOVE
Locate the shell script twitter/Glove-1.2/demo.sh, and set the parameter "CORPUS" to 
"CORPUS= ../your_preprocessed_output.csv" To train the GloVe model on your corpus, type in terminal:
```linux
cd GloVe-1.2
./demo.sh
```
In the future, we will work on making this process more automated. From here, there are several options you have.
You can (1) Find closest words to a given keyword using cosine similarity (twitter/word_dist.py), (2) Visualize words in k-means clusters containing a certain keyword (twitter/word_dist.py), or (3) visualize a word cloud of your top keywords based on cosine similarity. 

fill in... (update all scripts)
### Finding new keywords


### Visualize Clusters 


### Word Cloud  
