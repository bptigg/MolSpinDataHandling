import msdh
import Interpretor

def PrintFiles(filelist : list):
    i = 1
    for f in filelist:
        print(str(i) + ". " + f)
        i += 1

def main():
    files = msdh.ListFiles()
    PrintFiles(files)
    #file = int(input("Choose file (1-" + str(len(files)) + "): ")) - 1
    #msdh.time_evo_npz(files[file])
    #msdh.time_evo_npz(files[0])
    Interpretor.loop()

main()