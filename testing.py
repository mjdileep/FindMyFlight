__author__ = 'ASUS-PC'

from FindMyFlight.query_matcher import QueryMatcher
#this will generate the mysql query according to the user queries
#knowledge be added in the Data file
#that spacy.io is bit slow and it's entity recognition is also not good enough
from spacy.en import English
nlp=English()
var =QueryMatcher(nlp)
import requests

stmnt="Want to go from Boston to Denmark?"
results=var.getResults(stmnt)
print(results)
