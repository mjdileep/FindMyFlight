__author__ = 'ASUS-PC'
from FindMyFlight.query_matcher import QueryMatcher
from FindMyFlight.post_processor import postProcessor
from spacy.en import English
import copy
import pprint
class findFlights(object):
    nlp=None
    def __init__(self):
        self.nlp=English()
    def getFlights(self,statement):
        pp=postProcessor()
        var =QueryMatcher(self.nlp)
        results=var.getResults(statement)
        res=pp.process(results,1)
        return copy.deepcopy(res)

var=findFlights()
inp=input("enter")
var.getFlights(inp)