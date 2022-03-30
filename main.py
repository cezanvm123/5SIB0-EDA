import datetime
from DAGModel import DAGModel
import GradientDescentMT 
from RandomSolution import RandomSolution
from GradientDescentSolver import GradientDescent
import SettingFileParser


#numpy probably for math 

dag = DAGModel("Input\DAG.txt")
model = SettingFileParser.parseSettingFile(r"Input\xcps.setting", dag.getMovingResources(), "Input/costs.json")

randomTest = 1
gradientTest = 0
gradientMTTest = 0



# This calculates the durations of the moving nodes, this can be done everytime the velocities are changed in the settingmodel\
# It is a seperate function call as it needs the settingmodel to be initialized.
dag.calcMovingNodeDurations(model)
print()
# costs and makespan can only be determined after calcMovingDurations.
# !!!! if the velocities are changed calcMovingDurations HAS TO BE CALLED
print("Initial Machine cost is: %s euro" %(model.getMachineCost()))
print("Initial Machine makespan is: %s ms" %(dag.determineMakespan()))
print("Initial Gradient is: %s " %(dag.getGradient()[0]))



if randomTest :
    #The first optimization solution
    print("\nStart random optimization:")
    randomStart = datetime.datetime.now()
    randSol = RandomSolution()
    randSol.solve(model, dag)
    randomStop = datetime.datetime.now()
    print("\nRandom optimization makespan: %s at %s€" %(randSol.bestMake, randSol.cost))
    print(randSol.bestVel)
    print("Best Gradient is: %s " %(dag.getGradient()[0]))
    randomDelta = randomStop - randomStart
    print ("Random optimization took: %s s" %(randomDelta.seconds))

if gradientTest : 
    # #Gradient descent optimization solution
    print("\nStart gradient descent optimization:")
    gradientStart = datetime.datetime.now()
    gradDescSol = GradientDescent()
    gradDescSol.solve(model, dag)
    gradientStop = datetime.datetime.now()
    print("\nGradient Descent optimization makespan: %s at %s€" %(gradDescSol.bestMake, gradDescSol.cost))
    print(gradDescSol.bestVel)
    print("Best Gradient is: %s \n\n\n" %(dag.getGradient()[0]))

    gradientDelta = gradientStop - gradientStart
    print("Gradient descent took: %s s" %(gradientDelta.seconds))




if gradientMTTest : 
    if __name__ == '__main__':
        processes = 15
        gradientMTStart = datetime.datetime.now()
        GradientDescentMT.gradientMTsolve(model, dag, processes)
        gradientMTStop = datetime.datetime.now()
        
        gradientMTDelta = gradientMTStop - gradientMTStart

        print("Gradient descent multiprocess with process count: %s took: %s s" %(processes, gradientMTDelta.seconds))


print("done")