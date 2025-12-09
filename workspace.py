import msdh
import os

def LoadWorkSpace(filename : str):
    files = []
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
