__author__ = 'ASUS-PC'

from FindMyFlight.query_matcher import QueryMatcher
#this will generate the mysql query according to the user queries
#knowledge be added in the Data file
#that spacy.io is bit slow and it's entity recognition is also not good enough
from spacy.en import English
nlp=English()
var =QueryMatcher(nlp)
import requests

stmnt="What are the minimum price tickets from Colombo to India on 12-12-2016 ?"
results=var.getResults(stmnt)
print(results)
