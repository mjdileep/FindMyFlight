__author__ = 'ASUS-PC'

from FindMyFlight.query_matcher import QueryMatcher
#this will generate the mysql query according to the user queries
#knowledge be added in the Data file
#that spacy.io is bit slow and it's entity recognition is also not good enough
from spacy.en import English
nlp=English()
var =QueryMatcher(nlp)

stmnt="Want to go to New York on 12-11-2016 "
query,score=var.getQuery(stmnt)
print("user query: ",stmnt)
print("mysql query: ",query)
print("score: "+str(score))

stmnt="What is the cheapest flight available to fly to India on 16-12-2016 ? "
query,score=var.getQuery(stmnt)
print("user query: ",stmnt)
print("mysql query: ",query)
print("score: "+str(score))

stmnt="What are the tickers available for less than $500 from Boston to Colombo on 11-03-2016 ? "
query,score=var.getQuery(stmnt)
print("user query: ",stmnt)
print("mysql query: ",query)
print("score: "+str(score))

stmnt="is there any flights on 12-11-2016 to Japan? "
query,score=var.getQuery(stmnt)
print("user query: ",stmnt)
print("mysql query: ",query)
print("score: "+str(score))
import nltk
