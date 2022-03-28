from DAGModel import DAGModel
import GradientDescentMT 
from RandomSolution import RandomSolution
from GradientDescentSolver import GradientDescent
import SettingFileParser


#numpy probably for math 

dag = DAGModel("Input\DAG.txt")
model = SettingFileParser.parseSettingFile(r"Input\xcps.setting", dag.getMovingResources(), "Input/costs.json")

randomTest = False
gradientTest = False
gradientMTTest = True



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
    randSol = RandomSolution()
    randSol.solve(model, dag)
    print("\nRandom optimization makespan: %s at %s€" %(randSol.bestMake, randSol.cost))
    print(randSol.bestVel)
    print("Best Gradient is: %s " %(dag.getGradient()[0]))

if gradientTest : 
    # #Gradient descent optimization solution
    print("\nStart gradient descent optimization:")
    gradDescSol = GradientDescent()
    gradDescSol.solve(model, dag)
    print("\nGradient Descent optimization makespan: %s at %s€" %(gradDescSol.bestMake, gradDescSol.cost))
    print(gradDescSol.bestVel)
    print("Best Gradient is: %s \n\n\n" %(dag.getGradient()[0]))

if gradientMTTest : 
    if __name__ == '__main__':
        GradientDescentMT.gradientMTsolve(model, dag, 15)


print("done")