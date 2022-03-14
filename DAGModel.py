

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
        print(self.movingResources)



    def extractMovingResources(self, line):
        
        if "move" in line: 
            split1 = line.split()
            split2 = split1[1].split(".")
            movingResource = split2[0]

            if movingResource not in self.movingResources : 
                self.movingResources.append(movingResource)
    


    def extractNodes(self, line) : 
        if "Node" in line and "->" not in line : 
            self.nodes.append(Node(line))

    
    #line input e.g: Node42->Node69
    
    def extractDependency(self, line): 
        if "->" in line :
            split1 = line.split("->")
            N1 = split1[0].replace("Node",'')
            N2 = split1[1].replace("Node",'')
            temp = self.getNodeByNr(int(N2))
            self.nodes[int(N1)-1].addDependency(temp)


    def getNodeByNr(self, nr) :
        for n in self.nodes :
            if n.nr == nr :
                return n

    def getMovingResources(self) :
        return self.movingResources

    nodes = []
    routes = []
    movingResources = []
    


class Node :

    def __init__(self, line) :
        self.line = line
        self.dependencies = []

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


    def addDependency (self, nr):
        self.dependencies.append(nr)

    def test(self, str):
        self.line = str

    nr = 0
    moving = False
    duration = 0
    startTime = 0
    endTime = 0
    dependencies = []
    line = ""


class Route : 

    nodes = []