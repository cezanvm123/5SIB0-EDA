import copy
from dataclasses import dataclass
import json
import multiprocessing
from multiprocessing.dummy import Array
import random
import math
import sys
from tokenize import String
import numpy as np
import time
from copy import deepcopy
import os
import shutil

from multiprocessing import Process

from pkg_resources import ResolutionError


import datetime

def gradientMTsolve(model, dag, t) :
    
    
    sys.setrecursionlimit(10000) 
    
    print("Solving multithreaded with %s threads" %(t))
    
    path = "Temp\\"
    try:
        os.mkdir(path) # make temp directory for the results
    except OSError as error:
        print(error)  


    ml = [model]
    dl = [dag]
    threads = []
    for i in range(t) : 

        m = deepcopy(ml)
        d = deepcopy(dl)
        workerFile = path + str(i) + ".json"
        workThread = Process(target=worker, args=(m[0], d[0], i, workerFile))
        threads.append(workThread)
        workThread.start()

    

    for x in threads:
        x.join()
        
    bestMake = 0
    bestCost = 0
    bestVel = []
    
    for i in range(t) : 
        p = path + str(i) + ".json"
        f = open(p, 'r')
        json_data = json.load(f)

        makespan = json_data['makespan']
        cost = json_data['cost']
        vel = json_data['velocities']
        if bestMake == 0 or makespan < bestMake:
            bestMake = makespan
            bestCost = cost
            bestVel = vel.copy()

    print("Best makespan: %s, at cost: %s " %(bestMake, bestCost) )
    print("With velocities:", end='')
    print(bestVel)   
    shutil.rmtree(path, ignore_errors=True)# Cleanup dir
    




def worker(model, dag, j, p):
    print("Worker %s started work" %(j))
    iter = 1000
    minvel = [140, 100, 240, 140, 140, 140, 140, 140, 140]

    vel = []
    bestVel = []

    vel = model.getVelocityVector()
    bestVel = [0] * len(vel)
    result = ThreadResult()
    result.makespan = 0
    result.cost = 0

    f = open(p, "w")


    i = 0
    while i <= iter:
        #if j == 0 :
          #  print("Worker %s at i: %s" %(j, i))
        random.seed(a=None, version=2)
        v = 0
        while v <= len(vel) - 1:
            vel[v] = (random.random() * 150) + minvel[v]
            v += 1

        t = gradientDescent(model, dag, vel, bestVel)

        if t == None : # I think this means that the cost > maxcost before the gradient if so go again
            continue

        if  result.makespan == 0 or t.makespan <  result.makespan:
            result.makespan = t.makespan
            result.cost = t.cost
            result.velocities = t.velocities.copy()
        i += 1
        #print("succes")
    
    data = {}
    data['makespan'] = result.makespan
    data['cost'] = result.cost
    data['velocities'] = result.velocities.tolist()
    jsonData = json.dumps(data)
    f.write(jsonData)
    print("Worker %s finished " %(j))



def gradientDescent(model, dag, vel, bestVel):
    maxcost = 100000
    iterations = 3000
    model.setVelocityVector(vel)
    cost = model.getMachineCost()
    if cost > maxcost:  # Checking cost constraint, done here to prevent errors instead of using the loop constraint
        return

    k = 0
    lr = 10
    prevcost = 0
    prevvel = []
    dag.calcMovingNodeDurations(model)
    make = dag.determineMakespan()

    
    
    bestMake = 0
    cost = 0


    # Gradient descent loop
    
    while not (cost > maxcost or k >= iterations):
        
        # if k > 50 and make > 58500 and cost/maxcost > 0.90 :
        #    # print("returning")
        #     return
        
        #w = datetime.datetime.now()
      #  lr = 10 * (1 - cost/maxcost) +0.1
        #a = datetime.datetime.now()    
        dag.calcMovingNodeDurations(model)
        #b = datetime.datetime.now()
        make = dag.determineMakespan()
       # c = datetime.datetime.now()

        gradient = dag.getGradient()[0]


        prevvel = vel
        vel = vel + np.divide(gradient, np.square(vel))*lr
        
       # e = datetime.datetime.now()
        model.setVelocityVector(vel)
       # f = datetime.datetime.now()
        
        
        prevcost = cost
        cost = model.getMachineCost()
        k+=1
        
      #  d = datetime.datetime.now()


        # whi = d - w
        # da = b - a 
        # ma = c - b
        # ve = f - e

    if bestMake == 0 or make < bestMake:
        bestVel = prevvel.copy()
        bestMake = make
        cost = prevcost

    r = ThreadResult
    r.makespan = copy.copy(bestMake)
    r.velocities = copy.copy(bestVel)
    r.cost = copy.copy(cost)

    
    return r




@dataclass
class ThreadResult : 
    velocities = []
    makespan = 0
    cost = 0
