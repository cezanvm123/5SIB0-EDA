from enum import Enum
from operator import mod
from pickle import GLOBAL
from ResourceModel import Axis, AxisType, Resource, ResourceModel
import string
import json

class SearchState(Enum): 
    GLOBAL = 1
    AXIS = 2
    P_OR_P = 3
    VELOCITY = 4
    POSITION = 5




def parseSettingFile(path, movingResources, CCPath):
    print("Parsing setting file")
    model = ResourceModel()
    running = False
    state = SearchState.GLOBAL

    DEBUG = False

    # temporary objects
    tempResource = None
    tempAxis = None

    #bracket counters
    brackets = 0
    aBrackets = 0 #axis specific brackets  

    file = open(path, "r")


    def setState(s) :
        nonlocal state
        nonlocal DEBUG
        if DEBUG :
            print("State change to: ", end = '')
            print(s)
        
        state = s

    def globalSearch(line) : 
        nonlocal brackets
        nonlocal state
        nonlocal tempResource

        for word in movingResources : 
            if word in line : 
                # global search over 
                tempResource = model.getResourceByName(word)
                brackets+=1
                setState(SearchState.AXIS)


    def axisSearch(line) :
        nonlocal aBrackets
        nonlocal state
        nonlocal tempAxis

        if "Axis" in line : 
            if 'X' in line : 
                tempAxis = Axis(AxisType.X)
            elif 'Y' in line :
                tempAxis = Axis(AxisType.Y)
            elif 'Z' in line : 
                tempAxis = Axis(AxisType.Z)
            
            aBrackets+=1
            setState(SearchState.P_OR_P)
            

    def ppSearch(line) : 
        nonlocal state

        if "Profiles" in line : 
            setState(SearchState.VELOCITY)
        elif "Positions" in line : 
            setState(SearchState.POSITION)


    def velocitySearch(line) :
        nonlocal tempAxis

        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace(',', '')
        split = line.split()
        
        i = 0
        while i < len(split):
            if split[i] == "V": 
                if split[i+1] == "=":
                    tempAxis.setVelocity(float(split[i+2]))
                    setState(SearchState.P_OR_P)
            i+=1
        

    def positionSearch(line) : 
        nonlocal tempAxis

        if '}' in line :
            setState(SearchState.P_OR_P)
            return

        split = line.split("=")
        name = split[0].translate({ord(c): None for c in string.whitespace})

        tempAxis.addPosition(name, float(split[1]))

    def bracketManager(line) :
        nonlocal brackets
        nonlocal state
        nonlocal tempResource

        if '{' in line : 
            brackets+=1
        elif '}' in line :
            brackets-=1
            
            if brackets == 0 :
                setState(SearchState.GLOBAL)
                tempResource = None

    def abracketManager(line) : 
        nonlocal state
        nonlocal aBrackets
        nonlocal tempResource
        nonlocal tempAxis

        if '{' in line : 
            aBrackets+=1
        elif '}' in line :
            aBrackets-=1

        if aBrackets == 0 :
            setState(SearchState.AXIS)
            tempResource.addAxis(tempAxis)
            model.updateResource(tempResource)
            tempAxis = None

    def retreiveCosts() : 
        with open(CCPath) as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
        
        resources = jsonObject['resources']
        for i in resources :
            name = i['name'] 
            r = model.getResourceByName(name)
            jsonAxes = i['axes']
            for ar in r.axes :
                for ja in jsonAxes : 
                    axisType = ja['axis']
                    if ar.type == ar.type.getTypeByString(axisType) : 
                        cc = ja['costCoefficient']
                        ar.costCoefficient = cc
            model.updateResource(r)


    for l in file: 

        if l == '\n' :  
            continue

        if state == SearchState.GLOBAL :
            globalSearch(l)
        
        elif state == SearchState.AXIS :
            axisSearch(l)
            bracketManager(l) 

        elif state == SearchState.P_OR_P : 
            ppSearch(l)
            bracketManager(l) 
            abracketManager(l)

        elif state == SearchState.VELOCITY : 
            velocitySearch(l)
            bracketManager(l) 
            abracketManager(l)

        elif state == SearchState.POSITION : 
            positionSearch(l)
            bracketManager(l) 
            abracketManager(l)
    
    retreiveCosts()

              

    
    print("Setting parse done")
    return model



    
#test 
#parseSettingFile(r"Input\xcps.setting",['Arm1', 'Turner', 'PickPlace', 'Arm2'] )