# generate random floating point values
from random import seed
from random import random
import math
import time

class RandomSolution : 

    def __init__(self) -> None:
        pass

    def solve(self, model, dag) : 
        #self.sinSolve(model,dag)
        self.realRandom(model,dag)
    
    def realRandom(self,model,dag) : 
        minvel = [140, 100, 240, 140, 140, 140, 140, 140, 140]
        iter = 750000

        self.vel = model.getVelocityVector()
        self.bestVel = [0] * len(self.vel)

        i = 0
        while i <= iter : 
            seed(i/self.vel[0]*self.vel[len(self.vel)-1])
            self.printProgressBar(i,iter)
            v = 0 
            while v <= len(self.vel)-1:
                self.vel[v] = (random()*200) + minvel[v]
                v+=1

            self.checkVelocities(model,dag)
            i+=1




    def sinSolve(self,model,dag) : 
        #Some magic numbers here
        iterations = 1000
        changes = 25 #500
        max = 300  #150
        min = 150

        self.vel = model.getVelocityVector()
        self.bestVel = [0] * len(self.vel)
        rand = [0] * len(self.vel)
        
        self.checkVelocities(model,dag)

        # create velocity storage list  
        # creare randomNr list 
        c = 0
        i = 0
        while c <= changes : 
            self.fillRandomVec(rand, 5, 0, c)
            self.printProgressBar(c,changes)
            while i <= iterations: 

                self.determineVel(rand, i, max, min)
                self.checkVelocities(model,dag)
                i+=1
            i = 0
            c+=1


    def printProgressBar (self,iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()


    def determineVel(self, rand, index, max, min): 
        i = 0
        index +=1
        while i <= len(self.vel)-1:

            # sin((r1*x) + r2) *(max - min) + min
            s = (((rand[i]*i)*index)) + (rand[(len(rand)-1) - i])
            self.vel[i] = ((math.sin(s)*(max-min)/2) + (max -(max-min)/2))

            i+=1



    # loop
    # v = vector 
    # u = upper bound 
    # l = lower bound
    # s = seed
    def fillRandomVec(self, v, u, l,s): 
        seed(s)
        i = 0
        while i <= len(v)-1:
            v[i] = (random()*(u-l)) + l
            i+=1
        #print(v)
        return v

    def checkVelocities(self, model, dag) : 
        model.setVelocityVector(self.vel)
        


        cost = model.getMachineCost()
        if( cost > 100000) :
            return
        dag.calcMovingNodeDurations(model)

        make = dag.determineMakespan()    
        if self.bestMake == 0 or make < self.bestMake : 
            self.bestVel = self.vel.copy()
            self.bestMake = make     
            self.cost = cost           

    vel = []
    bestVel = []
    bestMake = 0
    cost = 0
    