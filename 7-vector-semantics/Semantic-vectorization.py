# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     comment_magics: false
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# *ANYL 580: NLP for Data Analytics*
#
# # **Lecture 6: Vector Semantics**

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Topics
#
# - Semeval 2017
# - Features redux
# - Project #1
# - Feature engineering
# - Toolkits (so far)
# - Similarity
# - Vectorization
#  - Frequency
#  - One-hot encoding
#  - TF-IDF
#    - Weighted log odds
#  - PMI
#  - Distributed representation
#   - word2vec
#   - skip-gram
#   - doc2vec
# - Maxent (logistic regression) classifiers
# - Learning and Optimization
#  - Pipelines
#  - Grid search

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Semeval 2017
#
# ![](../images/semeval-framework.jpg)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# Stages of SemEval/Senseval evaluation workshops
#
# - Expression of interest
# - Time table
# - Plan to collection and annotate data
# - Gold files released to participants
# - Participants run a test
# - Organizers score answers and scores annoated and discussed at a workshop. Important to this process are shared, detailed papers and code for the purpose of advancing the state of the art and practice.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Why four ground truth data sets?
#
# <img src="../images/model-triple.png" width="400">

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# Image from: Bengfort, Bilbro, and Ojeda Applied Text Analysis with Python. 
#
# Further insights from Wickham (2015) [Visualizing Statistical Models: Removing the Blindfold](http://had.co.nz/stat645/model-vis.pdf), and Kumar, McCann, Naughton, and Patel (2015) [Model Selection Management Systems: The Next Frontier of Advanced Analytics](http://pages.cs.wisc.edu/~arun/vision/SIGMODRecord15.pdf).
#
# Note, we've been focused on the yellow box around feature engineering, but with the introduction of linear models in J&M chapter 5, we now have more choices in terms of algorithms -- both in the sort of model we can use (thus far, generative versus discriminative), but also in terms of the parameters of that model and how it's tuned to the particular data we are using. 
#
# The organizers of semeval 2017 released four gold data sets with the understanding that a testdev data set would be used against, perhaps, hundreds of test runs for **hyperparameter tuning** a day. Thus, train and dev are used to tune features, testdev for hyperparameter tuning, and test for runs against new data. We'll talk about hyperparameters a bit today in the context of maxent.
#
# That said, it's important that all data sets represent a common distribution. Errors in setting up evaluations have happened and will no doubt happen in the future. The statistical analyses you run to examine distributional properties of your data are important!

# %% [markdown]
# # Links to resources
#
# - Task page: http://alt.qcri.org/semeval2017/task4/index.php?id=data-and-tools
# - Test your skills!: https://competitions.codalab.org/competitions/15632
# - Task 4 (Twitter sentiment) Description: https://www.aclweb.org/anthology/S17-2088.pdf
#  - A: Given a tweet, decide whether it expresses POSITIVE, NEGATIVE or NEUTRAL sentiment.
#  - B: Given a tweet and a topic, classify the sentiment conveyed towards that topic on a two-point scale: POSITIVE vs. NEGATIVE.
#  - C: Given a tweet and a topic, classify the sentiment conveyed in the tweet towards that topic on a five-point scale: STRONGLYPOSITIVE, WEAKLYPOSITIVE, NEUTRAL, WEAKLYNEGATIVE, and STRONGLYNEGATIVE.
#  - D: Given a set of tweets about a topic, estimate the distribution of tweets across the POSITIVE and NEGATIVE classes.
#  - E: Given a set of tweets about a topic, estimate the distribution of tweets across the five classes: STRONGLYPOSITIVE, WEAKLYPOSITIVE, NEUTRAL, WEAKLYNEGATIVE, and STRONGLYNEGATIVE.
#  
#  For both English and Arabic.
#  
#  You competed in Task 4A!

# %% [markdown]
# # How did the teams do?
# <img src="../images/semeval-scores.png" width="400">

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# For English the best ranking teams were BB twtr and DataStories, both achieving a macroaverage recall of 0.681. Both top teams used deep learning.
#
# Three of the top-10 scoring teams (INGEOTEC, SiTAKA, and UCSC-NLP) used SVM classifiers instead, with various surface, lexical, semantic, and dense word embedding features. The use of ensembles clearly stood out, with five of the top-10 scoring systems (BB twtr, LIA, NNEMBs, Tweester, and INGEOTEC) using ensembles, hybrid, stacking or some kind of mix of learning methods.
#
# Can you see why AVEREC is useful? Note that a few teams did not beat the baseline F1 score or accuracy score. How did you do?

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Some participant papers
#
# - [NILC-USP at SemEval-2017 Task 4: A Multi-view Ensemble for Twitter Sentiment Analysis](https://pdfs.semanticscholar.org/f649/33e626330997feb9ff3c1484da93127b88ab.pdf)  
#  - https://github.com/edilsonacjr/semeval2017
# - [TwiSE at SemEval-2016 Task 4: Twitter Sentiment Classification](https://arxiv.org/pdf/1606.04351.pdf)
# - https://github.com/balikasg/SemEval2016-Twitter_Sentiment_Evaluation
# - 🎓 [Minions at SemEval-2016 Task 4: or how to build a sentiment analyzer using off-the-shelf resources?](https://www.aclweb.org/anthology/S16-1038.pdf)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# - The first team used scikit-learn Linear Regression and Support Vector machines with three types of text representation:  1) bag-of-words model weighted by tf-idf; 2) average of the word embedding vectors of the words in the tweet and, 3) averaged weighted word embeddings of all words in the tweet with tf-idf weights. They supplemented features with sentiment lexicons.
#
# - Feature engineering of ngrams and sentiment lexicons for unigrams and bigrams. Bag-of-words with hashing representation. They used Logistic Regression and SVMs as base models and in an ensemble learning approach. They first generated a set of models that performed well as individual models, and then selected a subset of models that generate diverse outputs and combined them using an ensemble learning step with the intent to lower generalization error.
#
# - The third is a paper written by a team in a Master's program in Computational Linguistics in Romania. They used public APIs and tools including Alchemy API, sentiment140.com, and NLTK. 

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Project #1 Class Leaderboard

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Your Innovations

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Feature-based models
# - What features do I use? (selection)
# - How do I weigh features? 
# - How do I combine weights to make a prediction?

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# The idea of **feature selection** is to identify properties of a document that will likely contribute to classification as positive, negative, and neutral.
#
# Feature selection is useful for reducing the dimensionality of sample data and take advantage of words and other features that we know vary with respect to the task at hand.
#
# But we still need to quantify these features in such a way that we can distinguish the relative importance of words (again with respect to the task at hand). **Feature extraction** is concerned with  quantification and also further dimensionality reduction.
#
# And on top of this, we may need to **weight features, normalize, and regularize** so that we highlight the aspects we care about and also so that we avoid over-fitting to the sample data.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Feature Selection for Sentiment
# - Case (capitalization)
# - Previous word
# - Stemming, lemmatization
# - Unigrams, bigrams
# - Part-of-speech
# - Ontological information (e.g., part-whole relationships)
# - Lexical and syntactic features (e.g., adjectives, adverbs, terms near subjective expressions)

# %% {"slideshow": {"slide_type": "notes"}}
import nltk
import IPython
import os
from collections import Counter
from nltk.tree import Tree
from IPython.display import Image, display
from IPython.display import Image, display
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame


# %% {"slideshow": {"slide_type": "notes"}}
def jupyter_draw_nltk_tree(tree):
    cf = CanvasFrame()
    tc = TreeWidget(cf.canvas(), tree)
    tc['node_font'] = 'arial 13 bold'
    tc['leaf_font'] = 'arial 14'
    tc['node_color'] = '#005990'
    tc['leaf_color'] = '#3F8F57'
    tc['line_color'] = '#175252'
    cf.add_widget(tc, 10, 10)
    cf.print_to_file('tmp_tree_output.ps')
    cf.destroy()
    os.system('convert tmp_tree_output.ps tmp_tree_output.png')
    display(Image(filename='tmp_tree_output.png'))
    os.system('rm tmp_tree_output.ps tmp_tree_output.png')



# %% {"slideshow": {"slide_type": "slide"}}
# Tree - scope example

# They said NLU is amazing
# Going to class is 'meh', but NLU is amazing

tree = Tree.fromstring("""(4 (2 NLU) (4 (2 is) (4 amazing)))""")
jupyter_draw_nltk_tree(tree)

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Hand-built features
#
# - Lexicon-derived features
# - Negation
# - Modal adverbs:
#  - "It is **quite possibly** a masterpiece."
#  - "It is **totally amazing**"
# - Thwarted expectations:
#  - “Many consider the movie bewildering, boring, slow-moving or annoying.”
#  - “It was hailed as a brilliant, unprecedented artistic achievement worthy of multiple Oscars.”
# - Non-literal language:
#  - “Not exactly a masterpiece.”
#  - “Like 50 hours long.”
#  - “The best movie in the history of the universe.”

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# Examples from Chris Potts: http://web.stanford.edu/class/cs224u/materials/cs224u-2019-sentiment.pdf
#
# There is much more here on sentiment treebanks and using syntax for sentiment analysis.

# %% {"slideshow": {"slide_type": "slide"}}
# This example from https://scikit-learn.org/stable/modules/feature_selection.html

from sklearn.feature_selection import VarianceThreshold
X = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 1, 1], [0, 1, 0], [0, 1, 1]]
sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
sel.fit_transform(X)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# From: https://scikit-learn.org/stable/modules/feature_selection.html
#
# VarianceThreshold is a simple baseline approach to feature selection. It removes all features whose variance doesn’t meet some threshold. By default, it removes all zero-variance features, i.e. features that have the same value in all samples.
#
# As an example, suppose that we have a dataset with boolean features, and we want to remove all features that are either one or zero (on or off) in more than 80% of the samples. Boolean features are Bernoulli random variables, and the variance of such variables is given by
#
# so we can select using the threshold .8 * (1 - .8):

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Assessing feature functions
#
# - sklearn.feature_selection offers functions to assess how much information your feature functions contain with respect to your labels
#
# - But recall, features are not usually independent with respect to the class
#
# - Adding multiple feature *types (e.g., words and morphemes)* can lead to stronger correlations between features
#
# - Consider more holistic assessment methods: systematically removing or disrupting features in the context of a full model and comparing performance before and after.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Feature Extraction V1
# <img src="../images/text-vectorization.png" width="400">

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# Hopefully, during the course of thinking through a bag-of-words model for your project, you had the insight to add additional lexical resources to your model like this. While thus far we've simply thought of text vectorization as turning words into something we can compute -- there is more to it than this.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Feature Extraction - Deeper Dive
# <img src="../images/feature-extraction.png" width="400">

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# Image from: A Study of Feature Extraction techniques for Sentiment Analysis. https://arxiv.org/pdf/1906.01573.pdf
#
# In this diagram, there are three stage:
# 1. Pre-processing
# 2. Feature Extraction
# 3. Classification
#
# Between stage 1 and stage 2 is **selecting features** where you may be iteratively removing noise or patterns during model tuning. 
#
# From stage 2 to stage 3 is **feature extraction** and **weighting**. Feature extraction is the step where high dimensional features are mapped onto a set of low dimensional potential features for computing (classification). Weighting methods such as TF-IDF are used for ranking the relative importance of features.
#
# Finally, after stage 3 there is a consideration of fitting an algorithm and iterating over parameters and hyper-parameters.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Weights (parameters)
#
# ![](../images/term-weights.png)

# %% [markdown]
# Image from: J&M Chapter 5
#
# We'll go over Maxent (Logistic Regression) a bit later, but for now let's appreciate the view that this algorithms tunes by weighting terms for relative importance with respect to the task.
#
# The algorithm internal parameters (w) and bias term (b) in logistic regression are **parameters** selected in training.
#
# **Hyperparameters**, on the other hand, are configurations external to the model that are used in a final tuning stage. We'll talk briefly about these in grid search, below.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Toolkits
# ![](../images/toolkits.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# All of these steps can be accomplished with the toolkits we're using -- though often they are used in combination. I will show you some examples of this in a bit.
#
# We've already experimented with two out of three of these toolkits and will add one more for next week when we move to topic modeling.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ![](../images/compare-toolkits.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# From: https://medium.com/activewizards-machine-learning-company/comparison-of-top-6-python-nlp-libraries-c4ce160237eb
#
# Some other notes:
#
# | NLTK | Scikit-Learn | Gensim |
# |------|------|--------|
# | Big dependency | Not designed for text but with some NLP conveniences | Can serialize dictionaries and references in matrix market format (useful for multiple platforms) |
# | Designed for teaching | | |

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# Until now, we've touched on two different libraries for bag-of-words representation: NLTK and Scikit-Learn. Today we'll introduce a third and talk about some of the differences.
#
# While we're at it, we'll take a look at vectorization and feature extraction across all three toolkits.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Documents as Vectors
#
# ![](../images/doc-vector.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# For this section on vectorization using NLTK, Scikit-learn, and Gensim, code examples and images are drawn from: https://www.oreilly.com/library/view/applied-text-analysis/9781491963036/ch04.html
#
# Imagine the 1 dimensional vector as your vocabulary. The corpus has a length equivalent to the vocabulary. 
#
# So how best to represent a document as a vector? 

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Frequency
# ![](../images/token-frequencies.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# In fact, the *simplest encoding of semantic space is vocabulary*. 
#
# Thus, far we've used this insight in terms of the **bag-of-words** model. Documents that share many similar words are similar, in some sense. The BOW model represents text as a bag (or multi-set) of words after text pre-processing. From BOW, we can derive term frequencies for each word. 
#
# In this representation, each document is represented as a set of tokens and the value for each word position in the vector as its count. This is using a straight count. You could also normalize each count for the length of a document.

# %% {"slideshow": {"slide_type": "slide"}}
corpus = [
    'Microsoft On hold with support for 52 minutes now. Come on',
    'Beyond frustrated with my Xbox360 right now and that as of June Microsoft does not support it. Gotta find someone else to fix the drive',
    'Microsoft Heard you are a software company. Why then is most of your software so bad that it has to be replaced by 3rd party apps?'
]

corpus_alt = [
    "The elephant sneezed at the sight of potatoes.",
    "Bats can see via echolocation. See the bat sneeze!",
    "Wondering, she opened the door to the studio."
]

# %% {"slideshow": {"slide_type": "notes"}}
import nltk
from nltk.stem import WordNetLemmatizer
import string

#def tokenize(text):
#    stem = nltk.stem.SnowballStemmer('english')
#    text = text.lower()

#    for token in nltk.word_tokenize(text):
#        if token in string.punctuation: continue
#        yield stem.stem(token)


# the 'yield' statement indicates that this is a generator function
# https://coreyms.com/development/python-generators-how-to-use-them-and-the-benefits-you-receive
def tokenize(text):
    wnl = WordNetLemmatizer()
    text = text.lower()
    
    for token in nltk.word_tokenize(text):
        if token in string.punctuation: continue
        yield wnl.lemmatize(token)


# %% {"slideshow": {"slide_type": "slide"}}
tokens = map(tokenize, corpus)
for token in tokens:
    print(list(token))

# %% {"slideshow": {"slide_type": "slide"}}
# This is the data structure the NLTK SentimentAnalyzer used for our Naive Bayes example

from collections import defaultdict

def vectorize(doc):
    # set feature as 0
    features = defaultdict(int)
    for token in tokenize(doc):
        features[token] +=1
    return features


# %% {"slideshow": {"slide_type": "slide"}}
# creates an iterable of vectorized documents
# NLTK uses features in a dict object where the key is the name of the feature and the value 
# boolean or numeric.
vectors = map(vectorize, corpus)

for vector in vectors:
    print(vector)

# %% {"slideshow": {"slide_type": "slide"}}
# This is what we used for V2 of Naive Bayes using scikit-learn (and logistic regresion v1)
# The fit method expects an iterable or list of strings and creates a dictionary of the vocabulary
# of the corpus.

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
vectors = vectorizer.fit_transform(corpus)

# %% {"slideshow": {"slide_type": "slide"}}
print(vectorizer.vocabulary_)

# %% {"slideshow": {"slide_type": "slide"}}
# This is a sparse array where the index tuple is the doc ID and token ID from the dictionary
# and the value the count

for vector in vectors:
    print(vector)

# %% {"slideshow": {"slide_type": "slide"}}
# We'll be using Gensim next week. It's frequency encoder is doc2bow.
# It requires pre-tokenized documents
# To use doc2bow, we need a Gensim Dictionary that maps tokens to indices

import gensim

tokenized_corpus = [list(tokenize(doc)) for doc in corpus]
id2word = gensim.corpora.Dictionary(tokenized_corpus)

for doc in tokenized_corpus:
    print(id2word.doc2bow(doc))


# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ## One Hot Encoding
#
# ![](../images/one-hot.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# In this representation, word representations are normalized in terms of frequency of occurence. And because values are 0-1, this is a useful representation for neural networks.

# %% {"slideshow": {"slide_type": "slide"}}
# NLTK one-hot representation
# From our NLTK naive bayes example, recall that training_features[0] was ({'microsoft': True,'may': True},...},positive)
# We actually used a one-hot representation.

def vectorize(doc):
    return {
        token: True
        for token in doc
    }

vectors = map(vectorize, corpus)

# %% {"slideshow": {"slide_type": "slide"}}
for vector in vectors:
    print(vector)

# %% {"slideshow": {"slide_type": "slide"}}
# The only difference to the scikit-learn frequency based representation is 'binary=True'

vectorizer = CountVectorizer(binary=True)
vectors = vectorizer.fit_transform(corpus)

# %% {"slideshow": {"slide_type": "slide"}}
for vector in vectors:
    print(vector)

# %% {"slideshow": {"slide_type": "slide"}}
# Gensim does not have a one-hot encoder.
# doc2bow returns a list of tuples https://radimrehurek.com/gensim/corpora/dictionary.html
# We can use the dictionary to get a one-hot encoding vector.
# To get vectors, an inner list comprehension converts the list of tuples returned from the doc2bow method 
# into a list of (token_id, 1) tuples and the outer comprehension applies that converter to all documents 
# in the corpus. 
# Note that we don't get word similarity, but doc similarity.

import numpy as np

tokenized_corpus  = [list(tokenize(doc)) for doc in corpus]
id2word = gensim.corpora.Dictionary(tokenized_corpus)
vectors  = np.array([
    [(token[0], 1) for token in id2word.doc2bow(doc)]
    for doc in tokenized_corpus
    ])

# %% {"slideshow": {"slide_type": "slide"}}
for vector in vectors:
    print(vector)

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ## TF-IDF
#
# ![](../images/tf-idf.png)

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# **Term-Frequency Inverse Document Frequency** considers the relative frequency of terms in a document against term frequencies in other documents. 
#
# *The basic idea is that documents that are similar share terms that are common between them but more rare in other documents.*
#
# TF–IDF is computed for each term, such that the relevance of a token to a document is measured by the scaled frequency of the appearance of the term in the document, normalized by the inverse of the scaled frequency of the term in the entire corpus.

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# $$ tfidf( t, d, D ) = tf( t, d ) \times idf( t, D ) $$
#
# Where `t` denotes the terms; `d` denotes each document; `D` denotes the collection of documents.
#
# The first part (tf) is: 
# $$ tf(t,d)  $$
#
# - the number of times each word appeared in each document
#
# The second part (idf) is: 
#
# $$ idf( t, D ) = log \frac{ \text{| } D \text{ |} }{ 1 + \text{| } \{ d \in D : t \in d \} \text{ |} } $$
#
#
# - `D` is the document space, also equal to ${ d_{1}, d_{2}, \dots, d_{n} }$ where n is the number of documents in the collection. 
# - The denominator : $\text{| } \{ d \in D : t \in d \} \text{ |}$ is the total number of times in which term t appeared in all documents d (the ${d \in D}$ restricts the document to be in the current document space). Finally, '1' is added so as not to divide by zero.

# %% {"slideshow": {"slide_type": "slide"}}
# NLTK TextCollection does a number of nifty things such as concordancing, collocations, and tfidf.
# The function below yields a dictionary whose keys are terms and whose values are the TF–IDF 
# score for the term in that particular document.

from nltk.text import TextCollection

def vectorize(corpus):
    corpus_tokenized = [list(tokenize(doc)) for doc in corpus]
    texts  = TextCollection(corpus_tokenized)
    
    for doc in corpus_tokenized:
        return {
            term: texts.tf_idf(term, doc)
            for term in doc
        }


# %% {"slideshow": {"slide_type": "slide"}}
# Just the first doc here
vectors = vectorize(corpus)
for k, v in vectors.items():
    print(k, v)

# %% {"slideshow": {"slide_type": "slide"}}
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf  = TfidfVectorizer()
corpus_tfidf = tfidf.fit_transform(corpus)
print(corpus_tfidf)

# %% {"slideshow": {"slide_type": "slide"}}
corpus_tokenized  = [list(tokenize(doc)) for doc in corpus]
lexicon = gensim.corpora.Dictionary(corpus_tokenized)
tfidf   = gensim.models.TfidfModel(dictionary=lexicon, normalize=True)
vectors = [tfidf[lexicon.doc2bow(doc)] for doc in corpus_tokenized]

for vector in vectors:
    print(vector)

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # What TF-IDF does for us
#
# - Frequent terms contribute most to a document vector’s direction, but not all terms are relevant (“the”, “a”, ...).
#
# - It separates *important* terms from *frequent*, but irrelevant terms in the collection.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Maxent Classifiers
#
# The goal is to train a classifier that can make a binary decision about the class of a new input observation.
#
# ![](../images/maxent-formula.png)
#

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# ![](../images/maxent-score.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
#
#
# 1. For each $$f_i(x)$$ in a set of N features, determine if $$f_i(x)$$ should be 1 or 0.
# 2. Multiply each $$f_i(x)$$ with the associated weight $$w_i(d)$$, which depends on the decision d being evaluated.
# 3. Add up all of the weight*feature pairs: $$sum_d = \sum_{i=1}^{N} w_i(d)*f_i(x)$$
# 4. Exponentize (is that word?): $$numerator_d = \exp(sum_d) $$
# 5. Divide the sum by a number that will range the score between 0 and 1, and such that the sum of scores across all decisions is 1. 
#
# It turns out that this is the sum of the numerators for every possible decision d: $$denominator = \sum_{d} \exp(\sum_{i=1}^{N} w_i(d)*f_i(x))$$
#

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# Let a feature function, f_i(x), take in an input, x, and return either 0 or 1, depending if the feature is present in x
#
# ![](../images/maxent-feature.png)

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Define Features (with weights w)
#
# - Define features over data points
# - A feature doesn't have to be a word but might refer to words (e.g., word ends in -ing)
#
# - Spam/notspam example:
#  - w1(spam) (Email contains spelling/grammatical errors) .5
#  - w2(spam)(Email asks for money to be transferred) .2
#  - w3(spam) (Email mentions account holder’s name) -.5
#  - w1(notspam) (Email contains spelling/grammatical errors) -.2
#   - w2(notspam)(Email asks for money to be transferred) 0
#  - w3(notspam) (Email mentions account holder’s name) 1

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Multinomial Logistic Classifier 
# ![](../images/sigmoid.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# The multinominal logistic classifier uses a generalization of the sigmoid, called the softmax function, to compute the probability p(y = c|x). The softmax function takes a vector z = [z1,z2,...,zk] of k arbitrary values and maps them to a probability distribution, with each value in the range (0,1], and all the values summing to 1.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Maxent vs Naive Bayes
#
# - Naive Bayes
#  - Tries to **generate** observed data randomly
#  - Trained to maximize joint likelihood of data and classes: P(c,d)
#  - Features assumed to supply **independent evidence**
#  - Feature weights can be set independently
#  - Trained to maximize joint likelihood of data and classes: P(c,d)
#  - NB tends to overcount evidence
# - MaxEnt
#  - Tries to directly estimate the posterior probability. (**discriminates** between different outputs)
#  - Trained to maximize conditional likelihood of classes: P(c|d)
#  - Feature weights take **feature dependence** into account
#  - Feature weights must be mutually estimated
#  - Trained to maximize conditional likelihood of classes: P(c|d)
#  - Weights of features better model expectations

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Regularization
#
# Regularization is a way of finding a good **bias-variance tradeoff** by tuning the complexity of the model. 
# - collinearity (high correlation among features)
# - filter out noise from data
# - prevent overfitting
#
# The concept behind regularization is to introduce additional information (bias) to penalize extreme parameter weights.
#
# - L2 regularization (Euclidian distance)
# - L1 regularization (Manhatten distance)

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Scikit-learn
#
# - Regularization is applied by default
# - The parameter C is directly related to the regularization parameter λ as C=1/λ
# - For small values of C, we increase the regularization strength which will create simple models which may underfit the data. For large values of C, we allow more  model complexity and may overfit the data.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ## Pipelines
#
#

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ## Grid Search
#
#

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # A problem for TF-IDF
#
# ![](../images/tfidf-partisan.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# From [Fightin’ Words: Lexical Feature Selection and Evaluation for Identifying the Content of Political Conflict](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/81B3703230D21620B81EB6E2266C7A66/S1047198700002291a.pdf/fightin_words_lexical_feature_selection_and_evaluation_for_identifying_the_content_of_political_conflict.pdf) by Monroe, Colaresi, and Quinn 2008.
#
# While TF-IDF is particularly useful in retrieval tasks, it's not great for finding differences in text where the important words are shared across texts!
#
# The example from Monroe et al above is about looking at partisan differences in speeches. Both the Democratic and Republican parties talk about abortion (Democrats on the top half of the chart and Republicans on the bottom half of the chart).

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Remove stop words?
#
# - Elimnates important function words (inappropriately)
# - Elevates high-frequency non-stop words inappropriately (e.g., Senate)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# "We note, however, the practice of stop word elimination has been found generally to create more problems than it solves, across natural language processing applications. Manning et al. (2008) observe: ‘‘The general trend . . . over time has been from standard use of quite large stop lists (200–300 terms) to very small stop lists (7–12 terms) to no stop list whatsoever’’ (p. 27). They give particular emphasis to the problems of searching for phrases that might disappear or change meaning without stop words (e.g., ‘‘to be or not to be’’). In our example, a stop list would eliminate a word like her, which almost definitely has political content in the context of abortion,9 and a word like their, which might (e.g., women and their doctors)."

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# Often a solution has been to use Log-odds. 
#
# "With log-odds ratios, the sampling variation goes down with increased frequency. So, this measure will be inappropriately dominated by obscure words."
#
# Another fix is to try and the remove low-frequency words.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ## Weighted Log Odds
#
# ![](../images/log-odds.png)
# ![](../images/partisan-words.png)

# %% [markdown]
# The Monroe et al. method modifies log-odds in two ways:
#
# - it uses the z–scores of the log–odds–ratio, to controls for the amount of variance in a word’s frequency
# - it uses counts from a background corpus to provide a prior count for words, essentially shrinking the counts toward to the prior frequency in a large background corpus. 

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ![](../images/one-star-reviews.png)

# %% [raw] {"slideshow": {"slide_type": "notes"}}
# Here's another example from the article, [narrative framing of consumer sentiment in online restaurant reviews by Jurafsky, Chahuneau, Routledge, and Smith 2014](https://firstmonday.org/ojs/index.php/fm/article/view/4944/3863). 
#
# They also note that it's not enough to simply record the presence and absence of a word (feature). We also want to quantify information about different features. We may want to know the extent to which a word is used differently across two bodies of text.
#
# How do reviewers express fine–grained differences in sentiment beyond just positive or negative? 
#
# The initial investigation employed the “log odds ratio informative Dirichlet prior” method of Monroe, et al. (2008), to find words that are statistically overrepresented in a particular category of review compared to another (such as those with one star versus five stars, or reviewing cheap versus expensive restaurants). 
#
# These features enable differences even in very frequent words to be detected. Previous methods all have issues with frequently occuring words. 
#
# Because function words like pronouns and auxiliary verbs are both extremely frequent and [yet] have been shown to be important cues to social and narrative meaning, weighted log odds has utility for looking at fine-grained distinctions.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ## Positive Pointwise Mutual Information
#
# PPMI is a common measure for the strength of association between two words.
#
# ![](../images/ppmi.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# Counts of pairs of words getting the most and the least PMI scores in the first 50 millions of words in Wikipedia (dump of October 2015) filtering by 1,000 or more co-occurrences.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ![](../images/pmi.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# J&M note that negative values are problematic... how well could we do at the task of judging that things are occuring less than we'd expect through chance (unrelatedness)? 
#
# Thus, we just replace negative values with zero.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Similarity
#
# Let's take a break!

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # Senses
#
# ![](../images/senses.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# From: J&M https://web.stanford.edu/~jurafsky/slp3/slides/vector1.pdf
#
# - What do words mean? Often there are multiple senses. A **sense** is a meaning component.
# - There are also synonyms for senses that mean about the same thing, though they many not be appropriate for use in all of the same contexts (e.g., formal versus informal speech).

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# When we talk about similarity, we think about how words share some element of meaning. 

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # What does it mean to be similar? (Words)
#
# - Elizabeth, Liz, Lisa, Isabel (nicknames, variants)
# - Els + Libby + Bela (parts)
# - she, her, woman, girl (gender)
# - Queen, Saint, character in Jane Austen novel
# - English (language/culture)
# - name (description)
# - John (other names, contrasting male name)
# - "Who is she?" __ (semantic frame)
# - ...

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ![](../images/simlex.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# There is no objective measure of similarity. We often use human judgements for measures of similarity.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # The Linguistic Principle of Contrast
#
# > Every two forms contrast in meaning

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# ["This principle captures the insight that when speakers choose an expression, they do so because they mean something that they would not mean by choosing some alternative expression."](https://www.researchgate.net/profile/Eve_Clark/publication/20955529_On_the_pragmatics_of_contrast/links/552c32a40cf29b22c9c4434e.pdf)
#
# This applies to grammatical constructions, word choice, conventional expressions -- everything.
#
#

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# But Zellig Harris (1954): If A and B have almost identical environments we say that they are synonyms.
#
# Words are defined by their environments! (context)

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # How does this help?
#
# ![](../images/ongchoi.png)

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ![](../images/ongchoi2.png)

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ![](../images/learning.png)

# %% [markdown] {"slideshow": {"slide_type": "notes"}}
# There is a biological basis that accounts both for observations we can make around the nature of similarity, and also learning.

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ![](../images/distributional-hypothesis.png)

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # What does it mean to be similar (Documents)
#
# - Topics ("aboutness")
# - Genre
#     - novels, news, letters, reviews, play, poem, etc.
#     - horror, comedy, documentary, romance
# - Structure
#     - part-whole: headers, titles, signatures, paragraph
#     - functional: databases, texts, spreadsheets
# - Style 
#     - formal/informal, subjective/objective, etc.
# - Affect
#     - Happy, sad, angry, etc.
# - ... All the things we have talked about in the context of classification
