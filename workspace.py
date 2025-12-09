import msdh
import os

class workspace:
    def __init__(self, name, data, npzfile, key):
        self.name = name
        self.data = data
        self.datnpzfile = npzfile
        self.datakey = key
        pass

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
    return workspaces


