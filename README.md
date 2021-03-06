# TwitterStudiesCode


Read this guide for instructions on how best to utilize our code.

# Motivation 

In this repository, you will find code for an ongoing project to understand network effects, 
sentiment propogation, and trolling in a social media network, with 
the ultimate aim of proposing an AI-driven solution for online abuse. 
The current focus of our work is the 2017-present #MeToo twitter movement. 


## Recent Work 
See https://arxiv.org/abs/1911.05332 to read more about our ongoing work where we develop
natural language processing techniques to uncover keywords in #MeToo social media 
data for troll detection. Our keyword extraction methods currently utilize GloVe (Global Vectors for 
Word Representation), a renown word embedding model proposed in 2014 by Stanford Researchers.
See the explanation of the model here: https://nlp.stanford.edu/projects/glove/.


See https://polmeth2020.org/finding-social-media-trolls-dynamic-keyword-selection-methods-rapidly-evolving-online, 
our poster with findings from dynamic keyword selection when simulated on billions of historical #MeToo tweets and applied to realtime 
social media discussions on voting.

| Anti-movements  | #MeToo Begins | Hashtag Frequencies |
| ------------- | ------------- | ------------ |
|  <img src="/twitter/troll_example.png" width="300" height="300">   |  <img src="/twitter/WH_Oct17.png" width="300" height="300">   |  <img src="/twitter/freq-analysis.png" width="350" height="225">  |
| Examples of anti-feminist topics discovered through simulation of dynamic selection on historical twitter data. | Top hashtags in October 2017, the month #MeToo and related women empowerment hashtags began trending. | A glimpse into current work, involving augmenting dynamic selection with ML forecasting models.  |


## Included Code
This repo contains Stanford's GloVe implementation, as well as supplementary scripts written for our dynamic keyword selection method. In these additional scripts is code for preprocessing, forecasting (coming soon), discovering closest neighbors, and iteratively running our dynamic keyword selection over time with twitter API (coming soon). 
