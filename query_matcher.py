__author__ = 'ASUS-PC'
from FindMyFlight.json_handler import JsonHandler
from spacy.en import English
import copy,os
import spacy
import json,numpy
from datetime import datetime
from fuzzywuzzy import fuzz
from FindMyFlight.amadeus_handler import amadeusAdapter
class QueryMatcher(object):
    jsonHandler=JsonHandler()
    amd=amadeusAdapter("s9lQ77z7OKA0yGtJmjL1QmMPJr3a2y60")
    nlp=None
    with open(os.getcwd()+"/Data/IATA.json", 'r') as fp:
        iata = json.load(fp)
    def __init__(self,nlp):
        self.nlp=nlp
    def getResults(self,statement):
        properties=self.getProperties(statement)
        queries=self.searchPropertyMatch(properties)
        if len(queries)==0:
            return None,None
        maxQueryID,maxReplaces,maxScore=self.getBestQueryProperties(queries,statement)
        query,attributes,search=self.buildOriginalQuery(maxQueryID,maxReplaces)
        if search!="Error While Entity Parsing":
            return self.amd.search(search,attributes),maxScore,search
        else:
            return search,maxScore,search

    def getProperties(self,statement):

        doc=self.nlp(statement)
        properties={"date":"0","price":"0","airport":"0"}
        for each in doc.ents:
            if str(each.label_)=="MONEY":
                val=int(properties.__getitem__("price"))
                val+=1
                properties.__setitem__("price",str(val))
            elif str(each.label_)=="TIME" or str(each.label_)=="DATE" or str(each.label_)=="CARDINAL"or str(each.label_)=="QUANTITY" :
                val=int(properties.__getitem__("date"))
                val+=1
                properties.__setitem__("date",str(val))
            elif str(each.label_)=="GPE":
                val=int(properties.__getitem__("airport"))
                val+=1
                properties.__setitem__("airport",str(val))

        return properties

    def searchPropertyMatch(self,properties):
        queries=self.jsonHandler.matchProperties(properties)
        return queries

    def getBestQueryProperties(self,queries,statement):
        #do the partial matching for each query as well as the entity matching
        maxScore=0.0
        maxQueryID=""
        maxReplaces=None

        for ID in queries:
            totScore=self.getMaxHit(statement,self.jsonHandler.getGeneralizedQuery(ID))
            replaces=self.jsonHandler.getReplaces(ID)
            numOfReplaces=len(replaces)
            for i in range(0,len(replaces)):
                replace=entityCoordinate(replaces[i],i)
                score,key=self.getMaximumScoringKey(replace,statement,i)
                totScore+=score/numOfReplaces
                replaces[i]=key
            if(maxScore>=totScore):
                continue
            maxScore=totScore
            maxQueryID=ID
            maxReplaces=replaces
        return maxQueryID,maxReplaces,maxScore
    def getMaxHit(self,statement,generalizedQueries):
        maxScore=0.0
        queryList=generalizedQueries.split(",")
        for each in queryList:
            score=fuzz.partial_ratio(statement,each)
            if(score>maxScore):
                maxScore=score

        return maxScore
    def buildOriginalQuery(self,ID,replaces):
        if ID=="":
            return
        originalQuery=self.jsonHandler.getOriginalQuery(ID)
        attributes=self.jsonHandler.getAttributes(ID)
        search=self.jsonHandler.getSearchID(ID)
        for i in range(0,len(replaces)):
            if replaces[i]!=None:
                originalQuery=originalQuery.replace("xxx"+str(i),replaces[i])
                temp=attributes.get("xxx"+str(i))
                attributes.__delitem__("xxx"+str(i))
                attributes.__setitem__(temp,replaces[i])
            else:
                return originalQuery,attributes,"Error While Entity Parsing"


        return originalQuery,attributes,search

    def getMaximumScoringKey(self,replace,statement,i):

        #TODO implement the entity-coordination relationship
        if (replace.entity=="price"):
            doc=self.nlp(statement)
            for ent in doc.ents:
                if str(ent.label_)=="MONEY":
                    return 0,self.get_first_nbr_from_str(str(ent))
        elif (replace.entity=="date"):
            doc=self.nlp(statement)
            TIME=None
            indx=0
            positionScore=100000.0
            for ent in doc.ents:
                score=pow(replace.coordinate-indx,2)
                if str(ent.label_)=="DATE" or str(ent.label_)=="TIME" or str(ent.label_)=="CARDINAL" or str(ent.label_)=="QUANTITY" :
                    time=str(ent)
                    try:
                        time=datetime.strptime(time, "%d-%m-%Y").strftime('%Y-%m-%d')
                        if score<positionScore:
                            positionScore=score
                            TIME=time
                    except:
                        pass
                indx+=1
            return (20/(positionScore+1)),TIME
        elif (replace.entity=="airport"):
            doc=self.nlp(statement)
            indx=0
            GPE=None
            positionScore=100000.0
            for ent in doc.ents:
                score=pow(abs(replace.coordinate-indx),2)
                if str(ent.label_)=="GPE" and score<positionScore:
                    positionScore=score
                    GPE=str(ent)
                indx+=1
            return (20/(positionScore+1)),GPE

        else:
            categorySet=replace.entity.split(",")
            maxScore=0.0
            maxScoreReplace=""
            for each in categorySet:
                keySet=self.jsonHandler.getKeywordList(each)
                for eachInner in keySet:
                    score= fuzz.partial_ratio(eachInner,statement)
                    if score> maxScore:
                        maxScore=score
                        maxScoreReplace=eachInner
            return maxScore,maxScoreReplace

    def get_first_nbr_from_str(self,input_str):

        if not input_str and not isinstance(input_str, str):
            return 0
        out_number = ''
        for ele in input_str:
            if (ele == '.' and '.' not in out_number) or ele.isdigit():
                out_number += ele
            elif out_number:
                break
        return out_number
class entityCoordinate(object):
    entity=None
    coordinate=0
    def __init__(self,entity,coordinate):
        self.entity=entity
        self.coordinate=coordinate