
# time = 0 in ms
# if node.above == empty 
#   fire(time) 


# while running
#   running = false
#
#   for all n in nodes 
#       if !n.isDone
#           running = true
# 
#       fire = true
#
#       for all n.above 
#           if ! n.isDone(time)
#               fire is false 
#
#       if fire == true 
#           n.fire(time)
#
#       time +=1 


# for 




class Scheduler :

    def __init__(self, dag) :
        print("init")
        self.determineMakespan(dag)

            
    def determineMakespan(self,dag) : 
        for n in dag.nodes : 
            if len(n.dependenciesAbove) == 0 :
                n.fire(0)
        running = True
        while running :
            running = False
            
            for n in dag.nodes : 
                if n.endTime == 0 :# checks if one of the nodes isn't done yet if so we want another run
                    running = True

                if not n.endTime == 0 :
                    continue

                fin = True
                t = 0
                for a in n.dependenciesAbove: 
                    if a.endTime == 0 : 
                        fin = False
                    elif a.fired : 
                        if t < a.endTime:
                            t = a.endTime
                
                if fin : 
                    n.fire(t)
                    if self.makespan < n.endTime : 
                        self.makespan = n.endTime
                

        print("makespan: %s" %(self.makespan))
    makespan = 0
    criticalPath = []