__author__ = 'ASUS-PC'
import requests
from amadeus import Flights
flights=Flights("s9lQ77z7OKA0yGtJmjL1QmMPJr3a2y60")
class amadeusAdapter(object):
    def __init__(self,key):
        self.flights=Flights(key)
    def search(self,search,param):#inspiration search will be done according to user statements
        if search=="inspiration_search":
            resultsSet=[]
            origins=None
            destinations=None
            if param.get("origin")!=None:
                if param.get("origin")=="CMB":
                    origins=[{'label': 'Colombo - Bandaranayake International Air Port [CMB]', 'value': 'CMB'}]
                else:
                    origins=self.autoComplete(param.get("origin"))
            if param.get("destination")!=None:
                destinations=self.autoComplete((param.get("destination")))
            if len(origins)==0 :
                return None
            if destinations==None or len(destinations)==0:
                try:
                    param.__delitem__("destination")
                except:
                    pass
                for i in range(len(origins)):
                    param.__setitem__("origin",origins[i].get("value"))
                    resultsSet.append(self.inspiration_search(param))
                return resultsSet
            else:
                for i in range(len(origins)):
                    param.__setitem__("origin",origins[i].get("value"))
                    for j in range(len(destinations)):
                        param.__setitem__("destination",destinations[j].get("value"))
                        resultsSet.append(self.inspiration_search(param))
                return resultsSet

        elif search=="low_fare_search":
            resultsSet=[]
            origins=None
            destinations=None
            if param.get("origin")!=None:
                if param.get("origin")=="CMB":
                    origins=[{'label': 'Colombo - Bandaranayake International Air Port [CMB]', 'value': 'CMB'}]
                else:
                    origins=self.autoComplete(param.get("origin"))
            if param.get("destination")!=None:
                destinations=self.autoComplete((param.get("destination")))
            if len(origins)==0 or len(destinations)==0:
                return None
            else:
                for i in range(len(origins)):
                    param.__setitem__("origin",origins[i].get("value"))
                    for j in range(len(destinations)):
                        param.__setitem__("destination",destinations[j].get("value"))
                        resultsSet.append(self.low_fare_search(param))
                return resultsSet
        elif search=="extensive_search":
            resultsSet=[]
            origins=None
            destinations=None
            if param.get("origin")!=None:
                if param.get("origin")=="CMB":
                    origins=[{'label': 'Colombo - Bandaranayake International Air Port [CMB]', 'value': 'CMB'}]
                else:
                    origins=self.autoComplete(param.get("origin"))
            if param.get("destination")!=None:
                destinations=self.autoComplete((param.get("destination")))
            if len(origins)==0 or len(destinations)==0:
                return None
            else:
                for i in range(len(origins)):
                    param.__setitem__("origin",origins[i].get("value"))
                    for j in range(len(destinations)):
                        param.__setitem__("destination",destinations[j].get("value"))
                        resultsSet.append(self.extensive_search(param))
                return resultsSet
        return None
    def inspiration_search(self,param):
        return flights.inspiration_search(**param)
    def extensive_search(self,param):
        return flights.extensive_search(**param)
    def low_fare_search(self,param):
        return flights.low_fare_search(**param)
    def autoComplete(self,userTerm):
        return flights.auto_complete(term=userTerm)