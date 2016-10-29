__author__ = 'ASUS-PC'
from FindMyFlight.query_matcher import QueryMatcher
from FindMyFlight.post_processor import postProcessor
from spacy.en import English
import copy
import pprint
import numpy
class findFlights(object):
    nlp=None
    accuracy=[]
    def __init__(self):
        self.nlp=English()
    def getFlights(self,statement):
        pp=postProcessor()
        var =QueryMatcher(self.nlp)
        results,maxScore,search=var.getResults(statement)
        res=pp.process(results,search,1)
        return copy.deepcopy(res),maxScore
import sys
var=findFlights()
while 1:
    try:
        inp=input("Enter:")
        print(var.getFlights(inp))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        pass
