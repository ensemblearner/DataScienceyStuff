import operator
from collections import Counter
import math
import os
import numpy as np
"""
Needs further refactoring
v0.2
09/28/2013
Author: Mohitdeep Singh
"""

def load_dictionary(filename="data/dict.txt"):
    f = open(filename,"r")
    vector_list = sorted([ line.rstrip(os.linesep) for line in f])
    return np.ones(len(vector_list),float),vector_list
    #return np.array([1.0/len(vector_list)]*len(vector_list),float),vector_list



def generate_likelihood_distributions(document,label,feature_vectors, vector_list):
    feature_vector = feature_vectors[label]
    freqs = Counter(document.split())
    for word, frequency in freqs.items():
        index = vector_list.index(word.lower())
        feature_vector[index] +=  float(frequency)


def normalize_likelihood_vector(feature_vector):
    return feature_vector/len(feature_vector)

def assign_class_priors(labels):
    return Counter(labels)

def naive_bayes(document,priors,likelihood_dict,wordlist):
    probs = priors.copy()
    for k,v in probs.items():
        probs[k] = math.log(v)
    for word in document.split():
        for label in priors.keys():
            index = wordlist.index(word.lower())
            probs[label] += math.log(likelihood_dict[label][index])
    return probs

def get_class(prob_dict):
    return sorted(prob_dict.iteritems(), key=operator.itemgetter(1), reverse=True)[0]



"""
Main code starts from here!
"""

documents = ["This is awesome",
             "This is so cool email",
             "I won a lottery",
             "click to find more information",
             "lottery is send email",
             "win lottery here",
             "click on the link"
]
labels = ["ham","ham","ham","ham","spam","spam","spam"]


feature_vector, vector_list = load_dictionary()
unique_labels = list(set(labels))
feature_vector_dict = {label: feature_vector.copy() for label in unique_labels}

for label,document in zip(labels,documents):
    generate_likelihood_distributions(document,label,feature_vector_dict,vector_list)

for label, feature_vector in feature_vector_dict.items():
    feature_vector_dict[label] = normalize_likelihood_vector(feature_vector)

priors = assign_class_priors(labels)

test_string = "amazing information"
posteriors =  naive_bayes(test_string,priors,feature_vector_dict,vector_list)
print "prediction for ", test_string
print posteriors
print get_class(posteriors)
