__author__ = 'ASUS-PC'
import copy
import pprint
class postProcessor(object):
    init={"fare":{"total_price":"1000000.0"}}
    def __init__(self):
        pass
    def process(self,results,search,n):
        if search=="inspiration_search":
            targetFaults={'message': 'No result found.', 'more_info': 'No price result found.', 'status': 400}
            try:
                results.remove(targetFaults)
            except:
                pass
            if results==[]:
                return None
            return results
        minFareList=[]
        for i in range(n):
            minFareList.append(self.init)
        if results !=None and results!="Error While Entity Parsing":
            for each in results:
                if each!=None and each.get("status")!=400:
                    for el in each.get("results"):
                         self.insertQueue(el,minFareList)
        if minFareList[0]==self.init:
            return None

        return copy.deepcopy(minFareList)
    def insertQueue(self,element,minFareList):
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
    def printResults(self,minFareList,search):
        if search=="inspiration_search":
            print(minFareList)
            return
        for each in range(len(minFareList)):
            if minFareList[each]!=self.init:
                print("Total Fare = " ,minFareList[each].get("fare").get("total_price"))
                print(minFareList[each])
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
