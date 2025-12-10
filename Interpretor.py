import msdh
import workspace
import datafitting
from enum import Enum

class ACTION(Enum):
    HELP = -2
    EXIT = -1
    SAVE = 0
    LOAD = 1
    CREATE = 2
    PRINT = 3
    WORKSPACE = 4
    CURVEFIT = 5
    PLOT = 6
    DEFAULT = 7

class MODE(Enum):
    NotInString = 0
    InString = 1

class Task:
    def __init__(self, event : ACTION, arg : str):
        self.event = event
        self.args = arg


def KeywordCheck(input : str) ->list:
    char = []
    for c in input:
        char.append(c)
    #print(char)
    keywords = []
    args = []
    currentkeyword = ""
    currentargs = ""
    index = 0
    strmode = MODE.NotInString
    for c in char:
        if c == ' ':
            continue
        if c == '"' and strmode == MODE.NotInString:
            strmode = MODE.InString
            continue
        if c == '"' and strmode == MODE.InString:
            strmode = MODE.NotInString
            continue
        if c == ';':
            index += 1
            keywords.append(currentkeyword.lower())
            args.append(currentargs)
            currentkeyword = ""
            currentargs = ""
            continue
        if(strmode == MODE.NotInString):
            currentkeyword += c
        else:
            currentargs += c
    keywords.append(currentkeyword)
    args.append(currentargs)

    tasks = []
    index = -1
    for k in keywords:
        index += 1
        if k == 'help':
            return [ACTION.HELP]
        if k == 'exit':
            return [ACTION.EXIT]
        if k == 'save':
            tasks.append(Task(ACTION.SAVE, args[index]))
            continue
        if k == 'create':
            tasks.append(Task(ACTION.CREATE, args[index]))
            continue
        if k =='workspace':
            tasks.append(Task(ACTION.WORKSPACE, args[index]))
            continue
        if k == 'print':
            tasks.append(Task(ACTION.PRINT, args[index]))
            continue
        if k == 'plot':
            tasks.append(Task(ACTION.PLOT, args[index]))
            continue
        if k == 'curvefit':
            tasks.append(Task(ACTION.PLOT, args[index]))
            continue
            
    return tasks



def TaskHandling(tasks : list) ->bool:
    outcome = True
    for t in tasks:
        if(t.event == ACTION.SAVE):
            outcome = msdh.time_evo_npz(t.args)
        elif(t.event == ACTION.CREATE):
            outcome = workspace.CreateWorkSpace(t.args)
        elif(t.event == ACTION.PRINT):
            outcome == workspace.print_workspace(t.args)
        elif(t.event == ACTION.WORKSPACE):
            outcome = workspace.modify_workspace(t.args)
        elif(t.event == ACTION.CURVEFIT):
            outcome = datafitting.curvefit(t.args)

def help():
    help_str = """
    Info \n
    ----------------------
    SAVE - creates a NPZ file from the specified '.DAT' file\n
    LOAD
    """

def loop():
    input_str = ""
    event = ACTION.DEFAULT
    while(event != ACTION.EXIT):
        input_str = input(">>> ")
        events = KeywordCheck(input_str)
        if(len(events) == 0):
            continue
        if(events[0] == ACTION.EXIT):
            event = events[0]
            continue
        elif(events[0] == ACTION.HELP):
            help()
        else:
            TaskHandling(events)


    