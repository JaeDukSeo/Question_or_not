import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

# Voting classifiers
class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        try:
            return mode(votes)
        except:
            return "Neu"

    def confidence(self, features):
        votes = []
        try:
            for c in self._classifiers:
                v = c.classify(features)
                votes.append(v)

            choice_votes = votes.count(mode(votes))
            conf = choice_votes / len(votes)
            return conf
        except:
            return 0
# Function for getting features
def find_features_with(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features_with_stop:
        features[w] = (w in words)

    return features
def find_features_no(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features_no_stop:
        features[w] = (w in words)

    return features

# Load the two features
word_features5k_f = open("word_features_no_stop.pickle", "rb")
word_features_no_stop = pickle.load(word_features5k_f)
word_features5k_f.close()
word_features5k_f = open("word_features_with_stop.pickle", "rb")
word_features_with_stop = pickle.load(word_features5k_f)
word_features5k_f.close()

# Load all the with classifier
open_file = open("classifier_with.pickle", "rb")
classifier_with = pickle.load(open_file)
open_file.close()

open_file = open("MNB_classifier_with.pickle", "rb")
MNB_classifier_with = pickle.load(open_file)
open_file.close()

open_file = open("BernoulliNB_classifier_with.pickle", "rb")
BernoulliNB_classifier_with = pickle.load(open_file)
open_file.close()

open_file = open("LogisticRegression_classifier_with.pickle", "rb")
LogisticRegression_classifier_with = pickle.load(open_file)
open_file.close()

open_file = open("LinearSVC_classifier_with.pickle", "rb")
LinearSVC_classifier_with = pickle.load(open_file)
open_file.close()

open_file = open("SGDClassifier_classifier_with.pickle", "rb")
SGDC_classifier_with = pickle.load(open_file)
open_file.close()

# Load all the with classifier SGDClassifier_classifier_with.pickle
open_file = open("classifier_no.pickle", "rb")
classifier_no = pickle.load(open_file)
open_file.close()

open_file = open("MNB_classifier_no.pickle", "rb")
MNB_classifier_no = pickle.load(open_file)
open_file.close()

open_file = open("BernoulliNB_classifier_no.pickle", "rb")
BernoulliNB_classifier_no = pickle.load(open_file)
open_file.close()

open_file = open("LogisticRegression_classifier_no.pickle", "rb")
LogisticRegression_classifier_no = pickle.load(open_file)
open_file.close()

open_file = open("LinearSVC_classifier_no.pickle", "rb")
LinearSVC_classifier_no = pickle.load(open_file)
open_file.close()

open_file = open("SGDClassifier_classifier_no.pickle", "rb")
SGDC_classifier_no = pickle.load(open_file)
open_file.close()

# Make vote classifier
voted_classifier_with = VoteClassifier(
                                  classifier_with,
                                  SGDC_classifier_with,
                                  MNB_classifier_with,
                                  BernoulliNB_classifier_with,
                                  LogisticRegression_classifier_with,
                                  SGDC_classifier_with)

voted_classifier_no = VoteClassifier(
                                  classifier_no,
                                  SGDC_classifier_no,
                                  MNB_classifier_no,
                                  BernoulliNB_classifier_no,
                                  LogisticRegression_classifier_no,
                                  SGDC_classifier_no)

def sentiment(text):
    feats_with = find_features_with(text)
    feats_no   = find_features_no(text)

    class_with = voted_classifier_with.classify(feats_with)
    conf_with  = voted_classifier_with.confidence(feats_with) * 100
    class_no = voted_classifier_no.classify(feats_no)
    conf_no  = voted_classifier_no.confidence(feats_no) * 100

    return (class_with,conf_with,class_no,conf_no)
