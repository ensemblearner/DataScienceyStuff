from numpy import *
import operator
from collections import defaultdict

def createDataSet():
    X = array([[10.0,11],[1.0,1.0],[2,5],[1,0.1],[4,2.1]])
    y = ['A','A','B','B','A']
    return X,y
"""
Simple kNearest Neighbor Algorithm
"""
def classify(test_point, dataSet, labels, k=3):
    size = dataSet.shape[0]
    # Euclidean distance calculation
    distances =   (((tile(test_point, (size,1)) - dataSet)**2).sum(axis=1))**0.5
    # Initialize classcounter to 0
    classCount = {}
    classCount=defaultdict(lambda: 0, classCount)
    
    sortedDict = distances.argsort()
    #print sortedDict
    for i in range(k):
        vote = labels[sortedDict[i]]
        classCount[vote] +=1
    return sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)[0][0]



def main():
    X,y = createDataSet()
    test_point = [1,2]
    print classify(test_point,X,y)
main()
    

    
    