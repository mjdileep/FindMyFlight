__author__ = 'ASUS-PC'
from FindMyFlight.query_matcher import QueryMatcher
#this will generate the mysql query according to the user queries
#knowledge be added in the Data file
#that spacy.io is bit slow and it's entity recognition is also not good enough
from spacy.en import English
import copy
import pprint
nlp=English()
var =QueryMatcher(nlp)
init={"fare":{"total_price":"1000000.0"}}
minFareList=[]
for i in range(1):
    minFareList.append(init)
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
        if minFareList[0]!=init:
            for each in range(len(minFareList)):
                print("Total Fare = " ,minFareList[each].get("fare").get("total_price"))
                print("\nInbounds:")
                i=1
                for elm in minFareList[each].get("itineraries")[0].get("inbound").get("flights"):
                    print("\nFlight : ",i)
                    pprint.pprint(elm)
                    i+=1
                print("\nOutbounds:")
                i=1
                for elm in minFareList[each].get("itineraries")[0].get("outbound").get("flights"):
                    print("\nFlight : ",i)
                    pprint.pprint(elm)
                    i+=1