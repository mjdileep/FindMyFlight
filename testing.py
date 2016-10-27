__author__ = 'ASUS-PC'
from query_matcher import QueryMatcher

#this will generate the mysql query according to the user queries
#knowledge be added in the Data file
#that spacy.io is bit slow and it's entity recognition is also not good enough
var =QueryMatcher()
stmnt="is there any pizza less than 400 rupees?"
query,score=var.getQuery(stmnt)
print("user query: "+stmnt)
print("mysql query: "+query)
print("score: "+str(score))
import nltk
