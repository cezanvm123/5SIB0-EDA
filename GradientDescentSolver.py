# generate random floating point values
from random import seed
from random import random
import math
import numpy as np
import time



class GradientDescent:

    def __init__(self) -> None:
        pass

    def solve(self, model, dag):
        self.realRandom(model, dag)

    def realRandom(self, model, dag):

        iter = 1000
        minvel = [140, 100, 240, 140, 140, 140, 140, 140, 140]

        self.vel = model.getVelocityVector()
        self.bestVel = [0] * len(self.vel)

        i = 0
        while i <= iter:
            self.printProgressBar(i, iter)
            seed(time.time()*i/1000)
            v = 0
            while v <= len(self.vel) - 1:
                self.vel[v] = (random() * 100) + minvel[v]
                v += 1

            self.gradientDescent(model, dag)
            i += 1



    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
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
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

    def determineVel(self, rand, index, max, min):
        i = 0
        index += 1
        while i <= len(self.vel) - 1:
            # sin((r1*x) + r2) *(max - min) + min
            s = (((rand[i] * i) * index)) + (rand[(len(rand) - 1) - i])
            self.vel[i] = ((math.sin(s) * (max - min) / 2) + (max - (max - min) / 2))

            i += 1

    # loop
    # v = vector
    # u = upper bound
    # l = lower bound
    # s = seed
    def fillRandomVec(self, v, u, l, s):
        seed(s)
        i = 0
        while i <= len(v) - 1:
            v[i] = (random() * (u - l)) + l
            i += 1
        # print(v)
        return v


    def gradientDescent(self,model, dag):
        maxcost = 100000
        iterations = 3000
        model.setVelocityVector(self.vel)
        cost = model.getMachineCost()
        if cost > maxcost:  # Checking cost constraint, done here to prevent errors instead of using the loop constraint
            return

        k = 0
        lr = 10
        prevcost = 0
        prevvel = []
        dag.calcMovingNodeDurations(model)
        make = dag.determineMakespan()

        # Gradient descent loop
        while not (cost > maxcost or k >= iterations):
            dag.calcMovingNodeDurations(model)
            make = dag.determineMakespan()
            gradient = dag.getGradient()[0]
            prevvel = self.vel
            self.vel = self.vel + np.divide(gradient, np.square(self.vel))*lr
            model.setVelocityVector(self.vel)
            prevcost = cost
            cost = model.getMachineCost()
            k+=1

        if self.bestMake == 0 or make < self.bestMake:
            self.bestVel = prevvel.copy()
            self.bestMake = make.copy()
            self.cost = prevcost.copy()


    vel = []
    bestVel = []
    bestMake = 0
    cost = 0
