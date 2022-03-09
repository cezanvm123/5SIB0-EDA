from enum import Enum
from tkinter.messagebox import RETRY
from turtle import position

class Model: 
     
    def __init__(self) :
        self.resources = []


    def updateResourceByName(self, resource) : 
        print("updateResourceByName TODO")

    def getResourceByName(self, name):
        for r in self.resources :
            if r.getName() == name :
                return r
        
        r = Resource(name)
        self.resources.append(r)
        return r
        
    resources = []
    

class Resource: 

    def __init__(self, name) :
        self.name = name
        self.Axes = []

    def addAxis(self, axis) : 
        self.Axes.append(axis)  

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

    type = AxisType.X
    velocity = 0.0
    positions = []

class Position: 
    name = ""
    value = 0.0


