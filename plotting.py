import workspace
from datafit import DataFit
import matplotlib.pyplot as plt

class Data:
    def __init__(self):
        self.raw = []
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.name = ""
    def add(self,raw : workspace.workspace):
        self.raw = raw
        self.name = raw.name
    def setX(self, xcol):
        self.X = xcol
    def setY(self, ycol):
        self.Y = ycol
    def setZ(self, zcol):
        self.Z = zcol
class Plot:
    def __init__(self):
        self.figure = None
        self.axis = []
        self.Data = []
        return

    def AddAxis(self):
        if self.figure == None:
            return
        self.axis.append(self.figure.add_subplot(111))
        return

    def Initialize(self, figsize = (12,9)):
        self.figure = plt.figure(figsize=(12,9), dpi = 100)
        self.AddAxis()
        return
    
    def show(self):
        self.figure.show()
    
    def AddData(self, data : Data, axis):
        self.Data.append([data,axis])
        return
    
    def RemoveData(self, index : int):
        self.Data.pop(index)
        return
    
CurrentPlot = Plot()

#def InitializeFigure():
#    fig = plt.figure(figsize=(12,9), dpi = 100)
#    ax = fig.add_subplot(111)
#
#    global axis
#    global figure
#    axis.append([ax])
#    figure.append(fig)
#
#def plotdata(x,y):
#    axis[-1][0].plot(x,y)
#    plt.show()
#    return
#
#def GetData(data, xcol, ycol):
#    x = []
#    y = []
#    for i in range(1,len(data)):
#        x.append(data[i][xcol])
#        y.append(data[i][ycol])
#    return x,y

def PassArgument():
    keywords = ['figure', 'create', 'axis', 'in', 'using', 'add', 'remove', 'data', 'with'] #need to have a proper think about this (maybe too many words)
    plottypes = ['lines', 'scatter', 'contour']
    #example string "create figure using dataset1[1:2] with lines ; "in figure 1 add axis" ; "create figure 1 in axis 2 using dataset1[1:3] with lines"
    #


def plot(args):
    active = workspace.ACTIVE.AccessWorkspace()
    current = []
    for k in active:
        current.append(active[k])
    index = 0
    mode, cols = workspace.ACTIVE.GetModeColNum()
    #for i in cols:
    #    if i != mode:
    #        print("Workspace {} has a different number of cols than the avg, unexpected plotting may occur".format(current[index].name))
    #    index += 1
    #
    #x,y = GetData(current[0].data,0,1)
    #xf,yf = current[0].GetDataFit(0,1)[0].GetXY()
    #InitializeFigure()
    #plotdata(x,y)
    #plotdata(xf,yf)

    

    

    

