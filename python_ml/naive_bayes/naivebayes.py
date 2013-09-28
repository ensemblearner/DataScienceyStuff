import operator
from collections import Counter
import math
import os
import numpy as np
"""
Needs further refactoring
v0.3
09/28/2013
Author: Mohitdeep Singh
"""


class NaiveBayes:
    def __init__(self,dictionary = "data/dict.txt"):
        self._vector_list = self.__load_dictionary(dictionary)
        self.feature_vector = np.ones(len(self._vector_list),float)



    def __load_dictionary(self, filename):
        f = open(filename,"r")
        vector_list = sorted([ line.rstrip(os.linesep) for line in f])
        #print "Dictionary loaded!"
        return vector_list

    def train(self, documents,labels):
        assert len(documents) == len(labels)
        feature_vector_dict = self.__setup(labels)
        #print "training!"
        for document, label in zip(documents,labels):
            feature_vector = feature_vector_dict[label]
            freqs = Counter(document.split())
            for word, frequency in freqs.items():
                index = self._vector_list.index(word.lower())
                feature_vector[index] +=  float(frequency)
        self.feature_vector_dict = feature_vector_dict
        self.__normalize_likelihood_vector()

    def test(self,test_document):
        probs = self.priors.copy()
        for k,v in probs.items():
            probs[k] = math.log(v)
        for word in test_document.split():
            for label in probs.keys():
                index = self._vector_list.index(word.lower())
                probs[label] += math.log(self.feature_vector_dict[label][index])
        return probs

    def naive_bayes(test_document,priors,likelihood_dict,wordlist):
        probs = priors.copy()
        for k,v in probs.items():
            probs[k] = math.log(v)
        for word in test_document.split():
            for label in priors.keys():
                index = wordlist.index(word.lower())
                probs[label] += math.log(likelihood_dict[label][index])
        return probs

    def get_class(self,prob_dict):
        return sorted(prob_dict.iteritems(), key=operator.itemgetter(1), reverse=True)[0]

    def __setup(self, labels):
        self.__assign_class_priors(labels)
        unique_labels = list(set(labels))
        return {label: self.feature_vector.copy() for label in unique_labels}

    def __assign_class_priors(self, labels):
        self.priors =  Counter(labels)

    def __normalize_likelihood_vector(self):
        for label, feature_vector in self.feature_vector_dict.items():
            self.feature_vector_dict[label] = feature_vector/len(feature_vector)

def main():

    documents = ["This is awesome",
                 "This is so cool email",
                 "I won a lottery",
                 "click to find more information",
                 "lottery is send email",
                 "win lottery here",
                 "click on the link"
    ]
    labels = ["ham","ham","ham","ham","spam","spam","spam"]



    #----------------------------------------
    nb = NaiveBayes()
    nb.train(documents,labels)
    #print nb.feature_vector_dict
    test_cases = ["This is amazing","lottery email"]
    for test_case in test_cases:
        probs =  nb.test(test_case)
        print "this document is ", nb.get_class(probs)

if __name__ == "__main__":
    main()