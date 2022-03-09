from enum import Enum
from pickle import GLOBAL
from Model import Axis, AxisType, Resource, Model

class SearchState(Enum): 
    GLOBAL = 1
    AXIS = 2
    P_OR_P = 3
    VELOCITY = 4
    POSITION = 5




def parseSettingFile(path, movingResources):
    
    model = Model()
    running = False
    state = SearchState.GLOBAL

    # temporary objects
    tempResource = None
    tempAxis = None

    #bracket counters
    brackets = 0
    aBrackets = 0 #axis specific brackets  

    file = open(path, "r")


    def globalSearch(line) : 
        for word in movingResources : 
            if word in line : 
                print("succes")
                # global search over 
                tempResource = model.getResourceByName(word)
                brackets+=1
                state = SearchState.AXIS


    def axisSearch(line) :
        if "Axis" in line : 
            print("Axis found")
            if 'X' in line : 
                tempAxis = Axis(AxisType.X)
            elif 'Y' in line :
                tempAxis = Axis(AxisType.Y)
            elif 'Z' in line : 
                tempAxis = Axis(AxisType.Z)
            
            aBrackets+=1
            state = SearchState.P_OR_P
            

    def ppSearch(line) : 
        if "Profiles" in line : 
            state = SearchState.VELOCITY
        elif "Positions" in line : 
            state = SearchState.POSITION


    def velocitySearch(line) :
        line = line.replace('(', '')
        line = line.replace(')', '')
        split = line.split()

        for i in range(split.count) : 
            if split[i] == "V": 
                if split[i+1] == "=":
                    tempAxis.setVelocity(float(split[i+2]))

        print()


    def bracketManager(line) : 
        if '{' in line : 
            brackets+=1
        elif '}' in line :
            brackets-=1
            
            if brackets == 0 :
                state = SearchState.GLOBAL
                tempResource = None

    def abracketManager(line) : 
        if '{' in line : 
            abrackets+=1
        elif '}' in line :
            abrackets-=1
            
            if abrackets == 0 :
                state = SearchState.AXIS
                tempResource.addAxis(tempAxis)
                tempResource = None


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
            print("P_OR_P")

        elif state == SearchState.VELOCITY : 
            velocitySearch(l)
            bracketManager(l) 
            abracketManager(l)
            print("VELOCITY")

        elif state == SearchState.POSITION : 
            bracketManager(l) 
            abracketManager(l)
            print("POSITION")

              



    return model



    
#test 
parseSettingFile(r"Input\xcps.setting",['Arm1', 'Turner', 'PickPlace', 'Arm2'] )