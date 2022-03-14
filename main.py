import imp
from DAGModel import DAGModel
from Model import Model
import SettingFileParser


#numpy probably for math 

dag = DAGModel("Input\DAG.txt")
model = SettingFileParser.parseSettingFile(r"Input\xcps.setting", dag.getMovingResources())

# this calculates the durations of the moving nodes, this can be done everytime the velocities are changed in the settingmodel
dag.calcMovingNodeDurations(model)

#calculate node delays
print("done")