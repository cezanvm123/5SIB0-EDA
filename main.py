import imp
from DAGModel import DAGModel
from Model import Model
import SettingFileParser


dag = DAGModel("Input\DAG.txt")
model = SettingFileParser.parseSettingFile(r"Input\xcps.setting", dag.getMovingResources())

#calculate node delays
print("done")