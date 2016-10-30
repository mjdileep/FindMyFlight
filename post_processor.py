__author__ = 'ASUS-PC'
import copy
import pprint


class postProcessor(object):
    init = {"fare": {"total_price": "1000000.0"}}

    def __init__(self):
        self.replace = "Option "

    def process(self, results, search, n):

        if search == "inspiration_search":
            targetFaults = {'message': 'No result found.', 'more_info': 'No price result found.', 'status': 400}
            try:
                results.remove(targetFaults)
            except:
                pass
            if results == []:
                return None
            return results[0]

        if search == "low_transit_search":
            minItin = 1000
            minElement = {}
            if results != None and results != "Error While Entity Parsing":
                for each in results:
                    if each != None and each.get("status") != 400:
                        for el in each.get("results"):
                            for intin in el.get("itineraries"):
                                if len(intin.get("inbound").get("flights") + intin.get("outbound").get(
                                        "flights")) < minItin:
                                    minItin = len(
                                        intin.get("inbound").get("flights") + intin.get("outbound").get("flights"))
                                    minElement.__setitem__("fare", el.get("fare"))
                                    minElement.__setitem__("itineraries", [intin])
            if minElement == {}:
                return None
            return minElement

        minFareList = {}
        for i in range(n):
            minFareList.__setitem__(self.replace + str(i + 1), self.init)
        if results != None and results != "Error While Entity Parsing":
            for each in results:
                if each != None and each.get("status") != 400:
                    for el in each.get("results"):
                        self.insertQueue(el, minFareList)
        if minFareList.get(self.replace + str(1)) == self.init:
            return None

        return copy.deepcopy(minFareList.get(self.replace + str(1)))

    def insertQueue(self, element, minFareList):
        for i in range(len(minFareList)):
            price = float(element.get("fare").get("total_price"))
            exist = str(minFareList.get(self.replace + str(i + 1)).get("fare").get("total_price"))
            if float(exist) > price:
                for each in minFareList:
                    if element == each:
                        return
                for j in range(len(minFareList), i, -1):
                    minFareList.__setitem__(self.replace + str(j),
                                            copy.deepcopy(minFareList.get(self.replace + str(j - 1))))
                minFareList.__setitem__(self.replace + str(i + 1), copy.deepcopy(element))
                return

    def printResults(self, minFareList, search):
        if search == "inspiration_search":
            print(minFareList)
            return
        for each in range(len(minFareList)):
            if minFareList[each] != self.init:
                print("Total Fare = ", minFareList[each].get("fare").get("total_price"))
                print(minFareList[each])
                print("\nInbounds:")
                i = 1
                for elm in minFareList[each].get("itineraries")[0].get("inbound").get("flights"):
                    print("\nFlight : ", i)
                    pprint.pprint(elm)
                    i += 1
                print("\nOutbounds:")
                i = 1
                for elm in minFareList[each].get("itineraries")[0].get("outbound").get("flights"):
                    print("\nFlight : ", i)
                    pprint.pprint(elm)
                    i += 1
