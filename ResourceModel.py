from enum import Enum
from tkinter.messagebox import RETRY
from turtle import position

class ResourceModel: 
     
    def __init__(self) :
        self.resources = []


    def updateResource(self, resource) : 
        for r in self.resources :
            if r.getName() == resource.getName() :
                i = self.resources.index(r)
                self.resources[i] = resource
        

    def getResourceByName(self, name):
        for r in self.resources :
            if r.getName() == name :
                return r
        
        r = Resource(name)
        self.resources.append(r)
        return r

    def getResourceByLine(self, l) :
        for r in self.resources :
            if r.getName() in l :
                return r


    def getMachineCost(self) :
        c = 0
        for r in self.resources : 
            for a in r.axes : 
                c += (a.velocity * a.velocity) * a.costCoefficient
        
        return c

    def getVelocityVector(self) :
        l = []
        for r in self.resources : 
            for a in r.axes : 
                l.append(a.velocity)
        return l

    def setVelocityVector(self, v) : 
        i = 0
        for r in self.resources : 
            for a in r.axes : 
                a.setVelocity(v[i])
                i+=1


    def getGradientIndex(self, resource, axes):
        i = 0
        for r in self.resources :
            for a in r.axes :
                if(r == resource):
                    if axes ==1 and a.type==AxisType.X :
                        return i
                    elif axes ==2 and a.type==AxisType.Y :
                        return i
                    elif axes ==3 and a.type==AxisType.Z :
                        return i
                i+=1
        
    resources = []
    

class Resource: 

    def __init__(self, name) :
        self.name = name
        self.axes = []

    def addAxis(self, axis) : 
        self.axes.append(axis)  

    def getXVelocity(self): 
        for a in self.axes : 
            if a.type == AxisType.X :
                return a.velocity
    
    def getYVelocity(self): 
        for a in self.axes : 
            if a.type == AxisType.Y :
                return a.velocity

    def getZVelocity(self): 
        for a in self.axes : 
            if a.type == AxisType.Z :
                return a.velocity

    def getName(self) : 
        return self.name

    name = ""
    axes = []

class AxisType(Enum): 
    X = 1
    Y = 2
    Z = 3

    def getString(self, a) :
        if a == self.X :
            return 'X'
        elif a == self.Y :
            return 'Y'
        elif a == self.Z : 
            return 'Z'
    
    def getTypeByString(self, s) :
        if s == "X" or s == "x" :
            return self.X
        elif s == "Y" or s == "y" :
            return self.Y
        elif s == "Z" or s == "z" :
            return self.Z



class Axis:

    def __init__(self, type) :
        self.type = type
        self.positions = []

    def setVelocity(self, v): 
        self.velocity = v

    def addPosition(self, name, val) :
        pos = Position(name, val)
        self.positions.append(pos)

    type = AxisType.X
    velocity = 0.0
    positions = []
    costCoefficient = 0.0

class Position: 
    
    def __init__(self, name, value) :
        self.name = name
        self.value = value

    
    name = ""
    value = 0.0



