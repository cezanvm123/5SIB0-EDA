import imp
from DAGModel import DAGModel
from Model import Model
import SettingFileParser


#numpy probably for math 

dag = DAGModel("Input\DAG.txt")
model = SettingFileParser.parseSettingFile(r"Input\xcps.setting", dag.getMovingResources(), "Input/costs.json")

# This calculates the durations of the moving nodes, this can be done everytime the velocities are changed in the settingmodel\
# It is a seperate function call as it needs the settingmodel to be initialized.
dag.calcMovingNodeDurations(model)

# costs and makespan can only be determined after calcMovingDurations.
# !!!! if the velocities are changed calcMovingDurations HAS TO BE CALLED
print("Machine cost is: %s euro" %(model.getMachineCost()))
print("Machine makespan is: %s" %(dag.determineMakespan()))

#schedule = Scheduler(dag)

print("done")