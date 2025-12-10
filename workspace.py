import msdh
import os

class workspace:
    def __init__(self, name, data, npzfile, key):
        self.name = name
        self.data = data
        self.datnpzfile = npzfile
        self.datakey = key
        pass

class ActiveWorkspace:
    def __init__(self):
        self.workspaces = {}
        pass

    def AddWorkSpace(self, workspace : workspace):
        self.workspaces[workspace.name] = workspace
    def GetKey(self, index):
        i = 0
        for k in self.workspaces:
            if i == index:
                return k
            index += 1

    def RemoveWorkSpace(self, name):
        del self.workspaces[name]


LOADED_WORKSPACES = []
ACTIVE = ActiveWorkspace()

def CreateWorkSpace(filename : str):
    files = []
    workspaces = []
    root, ext = os.path.splitext(filename)
    ext = ext.lower()
    outcome = True
    if(ext != '.dat'):
        return False
    while files == []:
        files = msdh.ListCompatibleFiles(filename, ".npz")
        if(files == []):
            if(not msdh.time_evo_npz(filename)):
                return False
    if(len(files) == 1):
        print("Loading file: " + files[0])
        dat = msdh.LoadNPZ(files[0], 'dat')
        print("Creating workspace: " + root)
        workspaces.append(workspace(root, dat, files[0], 'dat'))
    
    for w in workspaces:
        LOADED_WORKSPACES.append(w)
    return True

def workspace_index(input : str):
    workspaces = []
    firstnum = ''
    lastnum = ''
    first = True
    inBrackets = False
    input = input + ','
    for c in  input:
        if c == ' ':
            continue
        if c == ':':
            first = False
            continue
        if c == '[':
            inBrackets = True
            continue
        if c == ']':
            inBrackets = False
            continue
        if c == ',' and inBrackets == False:
            value1 = int(firstnum) -1
            value2 = int(lastnum) -1
            for i in range(value1,value2+1):
                workspaces.append(i)
            firstnum = ''
            lastnum = ''
            first = True
        if(first and inBrackets):
            firstnum += c
        elif(inBrackets):
            lastnum += c
    return workspaces


def AddWorkspace():
    #get available spaces to load
    avail = []
    index = 0
    for w in LOADED_WORKSPACES:
        if w not in ACTIVE.workspaces:
            avail.append(w)
    if(len(avail) == 0):
        print("No available workspaces to load")
        return True
    for w in avail:
        index += 1
        print("{}. {}".format(index, w.name))
    print("Select workspaces (e.g. '[1:1],[3:5]' means add workspace 1 and add workspaces 3,4,5)")
    inputstr = input(">>> ")
    ws = workspace_index(inputstr)
    for w in ws:
        if(w < len(LOADED_WORKSPACES)):
            ACTIVE.AddWorkSpace(LOADED_WORKSPACES[w])
    


def RemoveWorkspace():
    avail = []
    index = 0
    for w in ACTIVE.workspaces:
        avail.append(w)
    if(len(avail) == 0):
        print("No available workspaces to remove")
        return True
    for w in avail:
        index += 1
        print("{}. {}".format(index, w))
    print("Select workspaces (e.g. '[1:1],[3:5]' means add workspace 1 and add workspaces 3,4,5)")
    inputstr = input(">>> ")
    ws = workspace_index(inputstr)
    for w in ws:
        if(w < len(ACTIVE.workspaces)):
            ACTIVE.RemoveWorkSpace(ACTIVE.GetKey(w))


def modify_workspace(args):
    funcs = [AddWorkspace, RemoveWorkspace]
    arguments = ['add', 'remove']
    index = 0
    outcome = True
    for a in arguments:
        if args == a:
            outcome = funcs[index]()
            break
        index += 1
    return outcome

def print_workspace(args):
    if args == 'loaded':
        print_loaded()
    elif args == 'active':
        print_active()
    else:
        print("Unrecogonsied command (arguments are 'loaded' or 'active')")
    return True

def print_loaded():
    index = 0
    if(len(LOADED_WORKSPACES) == 0):
        print("No workspace currently loaded")
    for w in LOADED_WORKSPACES:
        index += 1
        print("{}. {}".format(index, w.name))
    return True

def print_active():
    index = 0
    if(len(ACTIVE.workspaces)==0):
        print("No workspace currently active")
    for w in ACTIVE.workspaces:
        index += 1
        print("{}. {}".format(index, w))
    return True


