__author__ = 'ASUS-PC'
from FindMyFlight.query_matcher import QueryMatcher
#this will generate the mysql query according to the user queries
#knowledge be added in the Data file
#that spacy.io is bit slow and it's entity recognition is also not good enough
from spacy.en import English
import copy
nlp=English()
var =QueryMatcher(nlp)
elm={"fare":{"total_price":"1000000.0"}}
minFareList=[]
for i in range(10):
    minFareList.append(elm)
def insertQueue(element):
    for i in range(len(minFareList)):
        price=float(element.get("fare").get("total_price"))
        exist=str(minFareList[i].get("fare").get("total_price"))
        if float(exist)>price:
            for each in minFareList:
                if element==each:
                    return
            for j in range(len(minFareList),i,-1):
                minFareList[j-1]=copy.deepcopy(minFareList[j-2])
            minFareList[i]=copy.deepcopy(element)
            return


while 1:
    temp = input("Enter the query:")
    results=var.getResults(temp)
    if results !=None and results!="Error While Entity Parsing":
        for each in results:
            if each!=None and each.get("status")!=400:
                for el in each.get("results"):
                    insertQueue(el)
        for each in range(len(minFareList)):
            print(minFareList[each].get("fare").get("total_price")," ",minFareList[each])