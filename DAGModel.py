
import copy
from faulthandler import dump_traceback



class DAGModel :

    def __init__(self, DAGPath) :
        print("parsing DAG")

        f = open(DAGPath, "r")

        for l in f: 
            self.extractMovingResources(l)
            #maybe do this later when the settings file has been parsed
            self.extractNodes(l)
            self.extractDependency(l)

        print("DAG parse done")
        #print(self.movingResources)


    def calcMovingNodeDurations(self, settingModel) :

        self.gradient = [0]*(len(settingModel.getVelocityVector())+1)
        gradconstidx = len(settingModel.getVelocityVector())
        for n in self.nodes :
            if n.moving == False :
                n.gradi = gradconstidx
                n.grad = n.duration
                continue

            resource = settingModel.getResourceByLine(n.line)
            duration = 0

            # knowing the layout of the dag line the first two string splits are of no interest as shown below

            # |  0   |                              1                       |     2    |    3     |                       
            # Node114,move Arm1.XYZ to Before_Belt1 with speed profile normal,Arm1.X=263,Arm1.Y=200

            split = n.line.split(',') 
            i = 2
            while i < len(split):
                if 'X' in split[i]: 
                    s = split[i].split('=')
                    distance = int(s[1]) # distance the X axis moves in mm
                    t = distance / resource.getXVelocity()
                    if duration < t:
                        duration = t
                        n.gradi = settingModel.getGradientIndex(resource,1)
                        n.grad = distance

                
                elif 'Y' in split[i]: 
                    s = split[i].split('=')
                    distance = int(s[1]) # distance the Y axis moves in mm
                    t = distance / resource.getYVelocity()
                    if duration < t:
                        duration = t
                        n.gradi = settingModel.getGradientIndex(resource,2)
                        n.grad = distance

                elif 'Z' in split[i]: 
                    s = split[i].split('=')
                    distance = int(s[1]) # distance the Z axis moves in mm
                    t = distance / resource.getZVelocity()
                    if duration < t:
                        duration = t
                        n.gradi = settingModel.getGradientIndex(resource,3)
                        n.grad = distance


                i+=1
            
            n.duration = duration
        


    # this is needed for the settings file parse to know which resources to extract
    def extractMovingResources(self, line):
        
        if "move" in line: 
            split1 = line.split()
            split2 = split1[1].split(".")
            movingResource = split2[0]

            if movingResource not in self.movingResources : 
                self.movingResources.append(movingResource)
    

    # init the nodes list 
    def extractNodes(self, line) : 
        if "Node" in line and "->" not in line : 
            self.nodes.append(Node(line))

    
    #line input e.g: Node42->Node69
    
    def extractDependency(self, line): 
        if "->" in line :
            split1 = line.split("->")
            N1 = split1[0].replace("Node",'')
            N2 = split1[1].replace("Node",'')

            self.nodes[int(N1)-1].addDependencyBelow(self.getNodeByNr(int(N2)))
            self.nodes[int(N2)-1].addDependencyAbove(self.getNodeByNr(int(N1)))



    def getNodeByNr(self, nr) :
        for n in self.nodes :
            if n.nr == nr :
                return n

    # if a resource is moving it does not yet contain its duration
    def getMovingResources(self) :
        return self.movingResources





    def retreiveRoutes(self) : 
        
        for n in self.nodes :
            if len(n.dependenciesAbove) == 0 : 
                self.startPoints.append(n)
            elif len(n.dependenciesBelow) ==0 : 
                self.endPoints.append(n)

        for n in self.startPoints :
            r = Route(0,False)
            self.constructRoute(n, r)


        

    def constructRoute(self,node,route) :
        
        route.addNode(node)

        # More depedencies below spawn mode routes
        i = 1 
        while i < len(node.dependenciesBelow):
            self.constructRoute(node.dependenciesBelow[i], Route(route, True))
            i+=1


        if len(node.dependenciesBelow) >= 1 :
            self.constructRoute(node.dependenciesBelow[0], route)

        elif len(node.dependenciesBelow) == 0 : #reached the end leaf
            self.routes.append(route)
            
            if len(self.routes) % 10000 ==0 :
                print(len(self.routes))
            # for n in route.nodes :
            #     print(n.nr, end = ', ')
            # print()

    def resetTimes(self) : 
        for n in self.nodes : 
            n.startTime = 0
            n.endTime = 0

    def determineMakespanInit(self) : 
        self.resetTimes()
        makespan = 0
        prevn = 0
        self.critpath = []
        for n in self.nodes : 
            if len(n.dependenciesAbove) == 0 :
                n.fire(0)
                self.makespanOrder.append(n)
        running = True
        while running :
            running = False
            for n in self.nodes : 

                if not n.endTime == 0 :  # if the node has a endtime skip(continue) 
                    continue

                if n.endTime == 0 :# checks if one of the nodes isn't done yet if so we want another run
                    running = True

                fin = True
                t = 0
                for a in n.dependenciesAbove: 
                    if a.endTime == 0 : 
                        fin = False
                    elif a.fired : 
                        if t < a.endTime:
                            t = a.endTime
                            n.prev = a     # For construction of critical path, used for gradient
                
                if fin : 
                    n.fire(t)
                    self.makespanOrder.append(n)
                    if makespan < n.endTime : 
                        makespan = n.endTime
                        prevn = n

        while not prevn == 0:   # Constructs critical path
            self.critpath.append(prevn)
            prevn = prevn.prev

        self.updateGradient()

        return makespan

    def determineMakespan(self) : 
        if len(self.makespanOrder) == 0: 
            return self.determineMakespanInit()

        self.resetTimes()
        makespan = 0
        prevn = 0
        self.critpath = []

        for n in self.makespanOrder : 
            fin = True
            t = 0
            for a in n.dependenciesAbove: 
                if a.endTime == 0 : 
                    fin = False
                    print("order failed...")
                elif a.fired : 
                    if t < a.endTime:
                        t = a.endTime
                        n.prev = a     # For construction of critical path, used for gradient
                
            if fin : 
                n.fire(t)
                if makespan < n.endTime : 
                    makespan = n.endTime
                    prevn = n
        while not prevn == 0:   # Constructs critical path
            self.critpath.append(prevn)
            prevn = prevn.prev

        self.updateGradient()

        return makespan
    


    def updateGradient(self):
        for n in self.critpath:
            self.gradient[n.gradi] = self.gradient[n.gradi] + n.grad


    def getGradient(self):
        return self.gradient[:len(self.gradient)-1], self.gradient[-1]


    makespanOrder = []
    gradient = []
    nodes = []
    routes = [] #empty
    startPoints = []
    endPoints = []
    movingResources = []
    critpath = []
    



class Route : 

    def __init__(self, i, list) :
        if list == False :
            self.nodes = []
        else : 
            self.initList(i)
    
    def initList (self, r) : 
        self.nodes = []
        for n in r.nodes: 
            self.nodes.append(n)

    def addNode(self, n) :
        self.nodes.append(n)
    

    duration = 0
    movingPercentage = 0

    nodes = []



class Node :

    def __init__(self, line) :
        self.line = line
        self.dependenciesBelow = []
        self.dependenciesAbove = []

        self.gradi = 0
        self.grad = 0

        if "move" in line : 
            self.moving = True
        else :
            split = line.split(',')
            self.duration = float(split[1]) 
    
        self.setNr(line)
            
    def setNr(self, l) :
        split = l.split(',')
        num = split[0].replace("Node",'')
        self.nr = int(num)


    def addDependencyBelow (self, nr):
        self.dependenciesBelow.append(nr)

    
    def addDependencyAbove (self, nr):
        self.dependenciesAbove.append(nr)

# used when scheduling
    def fire(self,t) : 
        self.fired = True
        self.startTime = t
        self.endTime = t + self.duration*1000

    nr = 0
    moving = False
    prev = 0
    dependenciesBelow = [] #Outgoing arrows
    dependenciesAbove = [] #Incomming arrows
    line = ""

# will be used when scheduling 
    duration = 0
    startTime = 0
    endTime = 0
    fired = False


    
