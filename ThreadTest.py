import threading


def doWork(param,ind, name):
    param[ind] = name
    

arr=[]
arr = [0 for i in range(11)] 

for i in range(11) : 
    workThread = threading.Thread(target=doWork, args=(arr,i, i+1))
    workThread.start()

print(arr)

