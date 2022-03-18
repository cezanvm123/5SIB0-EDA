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
#dag.retreiveRoutes()

print("Machine cost is: %s euro" %(model.getMachineCost()))

print("done")