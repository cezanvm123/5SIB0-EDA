import imp
from DAGModel import DAGModel
from Model import Model
#import SettingFileParser


dag = DAGModel("Input\DAG.txt")
#model = Model(r"Input\xcps.setting", dag.getMovingResources())
#model = SettingFileParser.parseSettingFile(r"Input\xcps.setting", dag.getMovingResources())
print("done")