from pdb import line_prefix
import matplotlib.pyplot as plt

def plot(dag): 
    
    make = dag.determineMakespan()
    
    
    plt.figure(figsize=(1, 1), dpi=80)
    fig,gnt = plt.subplots()
    gnt.set_ylim(0,5)
    gnt.set_xlim(0,make)

    # Setting ticks on y-axis
    gnt.set_yticks([15, 30, 45, 60, 75])
    # Labelling tickes of y-axis
    gnt.set_yticklabels(['PP', 'T', 'A1', 'A2', 'R'])
    gnt.grid(True)
    

    for n in dag.nodes :
        if "PickPlace" in n.line: 
            gnt.broken_barh([(n.startTime, n.endTime)], (10, 9), facecolors =('tab:orange'))
        elif "Turner" in n.line : 
             gnt.broken_barh([(n.startTime, n.endTime)], (25, 9), facecolors =('tab:blue'))
        elif "Arm1" in n.line : 
            gnt.broken_barh([(n.startTime, n.endTime)], (40, 9), facecolors =('tab:red'))
        elif "Arm2" in n.line : 
            gnt.broken_barh([(n.startTime, n.endTime)], (55, 9), facecolors =('tab:green'))
        else :
            gnt.broken_barh([(n.startTime, n.endTime)], (70, 9), facecolors =('tab:grey'))


    plt.savefig("gantt1.png")
