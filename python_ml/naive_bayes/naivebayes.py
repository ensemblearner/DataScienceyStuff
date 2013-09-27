import operator

__author__ = 'Mohitdeep Singh'
from collections import defaultdict
from collections import Counter
import math

"""
Code to be refactored.
Initial commit!
"""

def create_word_vector(document,label, vector_space,total_words):

    for word in document.split():
        if word not in total_words: total_words.append(word)
        if label in vector_space and word in vector_space[label]:
            vector_space[label][word] +=1
        else:
            vector_space[label][word] = 1



def normalize_dict(dictionary,words= None):
    if words:
        vocab_cardinality = len(words)
        for word in words:
            if word not in dictionary:
                dictionary[word] = 1.0 / vocab_cardinality
    summation = sum(dictionary.values())
    for k,v in dictionary.items():
        dictionary[k] = v/float(summation)


def assign_class_priors(labels):
    return Counter(labels)

def naive_bayes(priors,likhoods,words):
    probs = priors.copy()
    #print probs
    for k,v in probs.items():
        probs[k] = math.log(v)
    #print probs
    for word in words:
        for label in priors.keys():
            probs[label] += math.log(likhoods[label][word])
            #probs[label] *=likhoods[label][word]
    return probs
def get_class(prob_dict):
    return sorted(prob_dict.iteritems(), key=operator.itemgetter(1),reverse=True)[0]


documents = ["This is awesome",
            "This is so cool email",
            "I won a lottery",
            "click to find more information",
            "lottery is send email",
            "win lottery here",
            "click on the link"
            ]
labels = ["ham","ham","ham","ham","spam","spam","spam"]
data_dict = defaultdict(list)
likhood = defaultdict(dict)
total_words = []
for label,document in zip(labels,documents):
    data_dict[label].append( create_word_vector(document,label, likhood,total_words) )

for label, feature in likhood.items():
    normalize_dict(feature,total_words)
#print likhood
priors =  assign_class_priors(labels)
normalize_dict(priors)
#print priors
posterior =  naive_bayes(priors, likhood, "click link lottery".split())
print get_class(posterior)