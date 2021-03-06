__author__ = 'ASUS-PC'
import copy
import json
import os
class JsonHandler(object):
    queries=open(os.getcwd()+"/Data/queries.json")#Path to json files
    keywords=open(os.getcwd()+"/Data/keywords.json")
    keywords=json.load(keywords)
    queries=json.load(queries)
    def matchProperties(self,properties):#properties is a json file
        queries=[]
        for each in self.queries.keys():
            flag=0
            for innerEach in self.queries.get(each).get("properties").keys():
                if(self.queries.get(each).get("properties").get(innerEach)==properties.get(innerEach)):
                    continue
                flag=1
                break
            if flag==0:
                queries.append(each)
        return copy.copy(queries)
    def getReplaces(self,ID):
        replaces=[]
        for each in sorted(self.queries.get(ID).get("replaces")):
            replaces.append(self.queries.get(ID).get("replaces").get(each))
        return copy.deepcopy(replaces)
    def getGeneralizedQuery(self,ID):
        return copy.deepcopy(self.queries.get(ID).get("GeneralForm"))
    def getOriginalQuery(self,ID):
        if(ID!=""):
            return copy.deepcopy(self.queries.get(ID).get("originalQuery"))
    def getAttributes(self,ID):
        if(ID!=""):
            return copy.deepcopy(self.queries.get(ID).get("attributes"))
    def getKeywordList(self,key):
        return copy.deepcopy(self.keywords.get(key).keys())
    def getSearchID(self,ID):
         if(ID!=""):
            return copy.deepcopy(self.queries.get(ID).get("search"))
    def addQueries(self,query):
        size=int(self.queries.get("size"))
        size+=1
        size=size.__str__()
        self.queries.__setitem__(size,query)
        self.queries.__setitem__("size",size)




