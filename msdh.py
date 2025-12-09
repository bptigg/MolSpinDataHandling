import numpy as np 
import os
import pandas as pd

def ListCompatibleFiles():
    files = os.listdir()
    compatible = []
    for f in files:
        root, ext = os.path.splitext(f)
        if ext == '.dat' or ext == '.DAT':
            compatible.append(f)
    return compatible

def time_evo_npz(filename : str):
    root, ext = os.path.splitext(filename)
    if not ext:
        return LoadDirectory()
    elif ext == '.dat' or ext == '.DAT':
        return LoadFile(filename, True)
    else:
        print(filename + " file not supported")
    return False

def LoadFile(filename : str, timevo = True):
    ds=pd.read_csv(filename, sep=r'[,|;\t" ]+(?=\S)', engine ='python')
    #if timeevo we split it into multiple files depending on the step
    data = []
    columns = ds.columns.values
    currentstep = 0
    steps = []
    for i in range(0,len(ds[columns[0]])):
        if ds[columns[0]][i] != currentstep:
            currentstep = ds[columns[0]][i]
            data.append([])
            if len(steps) == 0:
                steps.append(i+1)
            else:
                steps.append(i-[steps[-1]]+1)
    step = 0
    for s in steps:
        for i in range(s):
            values = ds.iloc[[i]]
            print(values)

    #if(timevo):


    print(ds)

def LoadDirectory(filename : str):
    return