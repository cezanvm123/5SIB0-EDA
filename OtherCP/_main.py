from DAGModel import DAGModel
import SettingFileParser

dag = DAGModel("DAG.txt")
model = SettingFileParser.parseSettingFile(r"xcps.setting", dag.getMovingResources(), "costs.json")
dag.calcMovingNodeDurations(model)
print("%s" %(dag.determineMakespan()))
#critical path finding
dag.pathmain()
print(dag.ctp)