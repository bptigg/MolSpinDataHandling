import workspace
from datafit import DataFit
import matplotlib.pyplot as plt

axis = []
figure = []

def InitializeFigure():
    fig = plt.figure(figsize=(12,9), dpi = 100)
    ax = fig.add_subplot(111)

    global axis
    global figure
    axis.append([ax])
    figure.append(fig)

def plotdata(x,y):
    axis[-1][0].plot(x,y)
    plt.show()
    return

def GetData(data, xcol, ycol):
    x = []
    y = []
    for i in range(1,len(data)):
        x.append(data[i][xcol])
        y.append(data[i][ycol])
    return x,y

def plot(args):
    active = workspace.ACTIVE.AccessWorkspace()
    current = []
    for k in active:
        current.append(active[k])
    index = 0
    mode, cols = workspace.ACTIVE.GetModeColNum()
    for i in cols:
        if i != mode:
            print("Workspace {} has a different number of cols than the avg, unexpected plotting may occur".format(current[index].name))
        index += 1
    
    x,y = GetData(current[0].data,0,1)
    xf,yf = current[0].GetDataFit(0,1)[0].GetXY()
    InitializeFigure()
    plotdata(x,y)
    plotdata(xf,yf)

    

    

    

