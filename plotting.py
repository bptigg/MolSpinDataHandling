import workspace
import action
from action import Node
from datafit import DataFit
import matplotlib.pyplot as plt

PlottingInterprator = None 
nodes = {}
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
    
class PlotTask():
    def __init__(self):
        pass
    
CurrentPlot = Plot()

top = ['create' , 'add', 'remove']
secondry = ['figure', 'axis', 'data', 'xtitle', 'ytitle', 'title']
tertiary = ['using', 'with', 'in']
types = ['lines', 'scatter', 'contour']

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

def PlotNetwork():
    global nodes
    for t in top:
        nodes[t] = Node(t)
    for s in secondry:
        nodes[s] = Node(s)
    for tr in tertiary:
        nodes[tr] = Node(tr)
    for ty in types:
        nodes[ty] = Node(ty)

    nodes['index'] = Node('index')
    nodes['str'] = Node('str')

    nodes['create'].AddChildren([nodes['figure']])
    temp = []
    for i in secondry[1:len(secondry)]:
        temp.append(nodes[i])
    nodes['add'].AddChildren(temp)
    temp = []
    for i in secondry:
        temp.append(nodes[i])
    for i in types:
        nodes[i].AddParents([nodes['with']])
    nodes['remove'].AddChildren(temp)
    temp = []

    nodes['figure'].AddParents([nodes['create'], nodes['remove'], nodes['in']])
    nodes['figure'].AddChildren([nodes['using'], nodes['index']])

    nodes['axis'].AddParents([nodes['add'], nodes['remove'], nodes['in']])
    nodes['axis'].AddChildren([nodes['using'], nodes['index']])

    nodes['using'].AddParents([nodes['figure'], nodes['index']])
    nodes['using'].AddChildren([nodes['index']])
    nodes['with'].AddParents([nodes['index']])
    nodes['with'].AddChildren(nodes[x] for x in types)
    nodes['in'].AddParents([nodes['index'], nodes['str']])
    nodes['in'].AddChildren([nodes['axis'], nodes['figure']])

    nodes['index'].AddParents([nodes['using'], nodes['figure'], nodes['axis'], nodes['data']])
    nodes['index'].AddChildren([nodes['with'], nodes['in']])
    nodes['str'].AddParents([nodes['xtitle'], nodes['ytitle'], nodes['title']])
    nodes['str'].AddChildren([nodes['in']])

    nodes['xtitle'].AddParents([nodes['add'], nodes['remove']])
    nodes['xtitle'].AddChildren([nodes['str']])
    nodes['ytitle'].AddParents([nodes['add'], nodes['remove']])
    nodes['ytitle'].AddChildren([nodes['str']])
    nodes['title'].AddParents([nodes['add'], nodes['remove']])
    nodes['title'].AddChildren([nodes['str']])

    global PlottingInterprator
    PlottingInterprator = action.Network(nodes)
    return

def ExceptionFunc(char : list):
    if char[0] == "[":
        return nodes['index']
    if char[0] == "'":
        return nodes['str']
    return None

def ValidateInput(words):
    if PlottingInterprator == None:
        PlotNetwork()

    nodes = PlottingInterprator.traverse(words, ExceptionFunc)

    if(not words[0] in top):
        return False
    if(not words[1] in secondry):
        return False
    EvaluateInput(nodes)

def EvaluateInput(validated):
    return True

def PassArgument(arg):    
    words = []
    chars = [[]]
    tempchars = []
    index = 0
    for c in arg:
        if c == ' ':
            chars[index].append(tempchars)
            tempchars = []
        elif c == ';':
            chars[index].append(tempchars)
            chars.append([])
            tempchars = []
            index = index + 1
        else:
            tempchars.append(c)
    chars[index].append(tempchars)
    print(chars)
    words = []
    index = 0
    for c in chars:
        words.append([])
        for c2 in c:
            if c2[0] == '[':
                words[index].append(c2)
            elif c2[0] == "'":
                words[index].append(c2)
            else:
                words[index].append(''.join(c2))
        index += 1
    print(words)
    valid = []
    for w in words:
        ValidateInput(w)





def plot(args):
    active = workspace.ACTIVE.AccessWorkspace()
    if len(active) == 0:
        return
    current = []
    for k in active:
        current.append(active[k])
    index = 0
    mode, cols = workspace.ACTIVE.GetModeColNum()
    PassArgument(args)
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

    

    

    

