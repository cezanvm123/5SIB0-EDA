from DAGModel import DAGModel
from RandomSolution import RandomSolution
import SettingFileParser


#numpy probably for math 

dag = DAGModel("Input\DAG.txt")
model = SettingFileParser.parseSettingFile(r"Input\xcps.setting", dag.getMovingResources(), "Input/costs.json")




# This calculates the durations of the moving nodes, this can be done everytime the velocities are changed in the settingmodel\
# It is a seperate function call as it needs the settingmodel to be initialized.
dag.calcMovingNodeDurations(model)
print()
# costs and makespan can only be determined after calcMovingDurations.
# !!!! if the velocities are changed calcMovingDurations HAS TO BE CALLED
print("Initial Machine cost is: %s euro" %(model.getMachineCost()))
print("Initial Machine makespan is: %s ms" %(dag.determineMakespan()))




#The first optimization solution
print("\nStart random optimization:")
randSol = RandomSolution()
randSol.solve(model, dag)
print("\nRandom optimization makespan: %s at %s€" %(randSol.bestMake, randSol.cost))
print(randSol.bestVel)





print("done")