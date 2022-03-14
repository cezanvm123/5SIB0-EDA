from enum import Enum
from tkinter.messagebox import RETRY
from turtle import position

class Model: 
     
    def __init__(self) :
        self.resources = []


    def updateResourceByName(self, resource) : 
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
        
    resources = []
    

class Resource: 

    def __init__(self, name) :
        self.name = name
        self.Axes = []

    def addAxis(self, axis) : 
        self.Axes.append(axis)  

    def getXVelocity(self): 
        for a in self.Axes : 
            if a.type == AxisType.X :
                return a.velocity
    
    def getYVelocity(self): 
        for a in self.Axes : 
            if a.type == AxisType.Y :
                return a.velocity

    def getZVelocity(self): 
        for a in self.Axes : 
            if a.type == AxisType.Z :
                return a.velocity

    def getName(self) : 
        return self.name

    name = ""
    Axes = []
    editable = False

class AxisType(Enum): 
    X = 1
    Y = 2
    Z = 3



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

class Position: 
    
    def __init__(self, name, value) :
        self.name = name
        self.value = value

    
    name = ""
    value = 0.0



