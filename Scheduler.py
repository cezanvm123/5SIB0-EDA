
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




class Scheduler :

    def __init__(self, dag) :
        print("init")

    def determineMakespan(self,dag) : 
        print("makespan")
        time = 0
        running = True

        for n in dag.nodes : 
            if len(n.dependenciesAbove) == 0 :
                n.fire(time)


        while running :
            print("running")
            running = False
            
            for n in dag.nodes :   
                if not n.isDone() :# checks if one of the nodes isn't done yet if so we want another run
                    running = True
                    
                



    makespan = 0
    criticalPath = []