from enum import Enum

class Model: 
    name = ""
    resources = []
    

class Resource: 
    name = ""
    Axes = []
    editable = False

class AxisType(Enum): 
    X = 1
    Y = 2
    Z = 3



class Axis:
    type = AxisType.X
    velocity = 0.0



