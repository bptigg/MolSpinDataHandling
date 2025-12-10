import numpy as np 
import os
import pandas as pd

def ListFiles():
    files = os.listdir()
    compatible = []
    for f in files:
        root, ext = os.path.splitext(f)
        if ext == '.dat' or ext == '.DAT':
            compatible.append(f)
    return compatible

def ListCompatibleFiles(filename : str, extension : str):
    files = os.listdir()
    root,ext = os.path.splitext(filename)
    compatible = []
    for f in files:
        root2,ext2 = os.path.splitext(f)
        if(ext2 == extension):
            compatible.append(root2)
    temp = []
    for f in compatible:
        char = 0
        notc = False
        for c in root:
            c2 = f[char]
            if c == c2:
                char += 1
                continue
            notc = True
        if(not notc):
            temp.append(f)
    compatible = temp
    return compatible
    

def time_evo_npz(filename : str):
    root, ext = os.path.splitext(filename)
    if not ext:
        return LoadDirectory()
    elif ext == '.dat' or ext == '.DAT':
        return LoadFile(filename, root, True)
    else:
        print(filename + " file not supported")
    return False

def LoadFile(filename : str, root : str, timevo = True):
    if(os.path.isfile(filename) == False):
        return False
    ds=pd.read_csv(filename, sep=r'[,|;\t" ]+(?=\S)', engine ='python')
    #if timeevo we split it into multiple files depending on the step
    data = [[]]
    columns = ds.columns.values
    currentstep = 1
    steps = []
    for i in range(0,len(ds[columns[0]])):
        if ds[columns[0]][i] != currentstep:
            currentstep = ds[columns[0]][i]
            data.append([])
            if len(steps) == 0:
                steps.append(i+1)
            else:
                steps.append(i-[steps[-1]]+1)
    if(len(steps) == 0):
        steps.append(len(ds[columns[0]]))
    else:
        steps.append(len(ds[columns[0]]) - steps[-1])
    step = 0
    for s in steps:
        for i in range(s):
            length = len(ds.iloc[[i]].values[0])
            values = ds.iloc[[i]].values[0][1:length]
            data[step].append(values)
    if(timevo):
        columns = columns[1:len(columns)]
        index = 0
        for d in data:
            d.insert(0,columns)
            npz = np.array(d)
            name = root + "-" + str(index)
            print("Saving NPZ file: " + name)
            np.savez_compressed(name,dat=npz, allow_pickle=True)
            index += 1
    return True

def LoadNPZ(filename : str, key : str):
    file = filename + ".npz"
    f = np.load(file, allow_pickle=True)
    print(f[key])
    return f[key]
        
            

def LoadDirectory(filename : str):
    return False