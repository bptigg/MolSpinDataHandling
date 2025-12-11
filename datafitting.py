from datafit import DataFit
from datafit import FitType as ft
from scipy import optimize as spo
import workspace
import numpy as np
import math
import plotting

#a valid argument will have the format: 'exp using [1,3,4]'
#this means, fit a exponential to the curve 
def InterperArgs(args):
    arglist = [c for c in args]
    fits = ['exp', 'linear', 'logarithmic', 'fft']
    strings = []
    fit = []
    using = []
    in_bracket = False
    current_string = ""
    for c in arglist:
        if c == '[':
            in_bracket = True
            continue
        if c == ']':
            in_bracket = False
            strings.append(current_string)
            current_string = ''
            continue
        if c == ',' and in_bracket == False:
            strings.append(',')
            current_string = ''
            continue
        if c == ' ' and in_bracket == False:
            if current_string == '':
                continue
            strings.append(current_string)
            current_string = ''
            continue
        current_string += c
    print(strings)
    count = 0
    xlist = []
    ylist = []
    for w in strings:
        if w == ',':
            count = 0
            continue
        if(count == 0):
            if(w in fits):
                fit.append(w)
                count += 1
                continue
            else:
                continue
        if(count == 1):
            if w == 'using':
                using.append(True)
            else:
                using.append(False)
            count += 1
            continue
        if(count == 2):
            first = ''
            last = ''
            firststr = True
            for c in w:
                if c == ':':
                    firststr = False
                    continue
                if firststr:
                    first += c
                    continue
                if not firststr:
                    last += c
                    continue
            firstval = int(first)
            lastvals = []
            seperators = []
            cstring = ""
            for c in last:
                if c == " ":
                    continue
                if c.isdigit():
                    cstring += c
                else:
                    lastvals.append(int(cstring))
                    if c == ',' or c == '-':
                        seperators.append(c)
                    cstring = ''
            lastvals.append(int(cstring))
            xlist.append(firstval)
            y = []
            for s in range(0,len(seperators)):
                if (seperators[s] == ','):
                    y.append(lastvals[s])
                else:
                    vals = [x for x in range(lastvals[s], lastvals[s+1])]
                    for x in vals:
                        y.append(x)
            y.append(lastvals[-1])
            ylist.append(y)
    return fit, xlist, ylist


def GetData(data, xcol, ycol):
    x = []
    y = []
    for i in range(1,len(data)):
        x.append(data[i][xcol])
        y.append(data[i][ycol])
    return x,y

def GetFitFunc(fitstr):
    fits = ['exp', 'fft']#, 'linear', 'logarithmic']
    fitfuncs = [exponential_fit,fft]
    index = 0
    for f in fits:
        if fitstr == f:
            return fitfuncs[index]
        index += 1
    return None


def curvefit(args):
    active = workspace.ACTIVE.AccessWorkspace()
    current = []
    for k in active:
        current.append(active[k])
    index = 0
    mode, cols = workspace.ACTIVE.GetModeColNum()
    for i in cols:
        if i != mode:
            print("Workspace {} has a different number of cols than the avg, unexpected datafitting may occur".format(current[index].name))
        index += 1
        
    fit, xlist, ylist = InterperArgs(args)
    index = 0
    for f in fit:
        x = []
        y = []
        fitfunc = GetFitFunc(f)
        if(fitfunc == None):
            continue
        for w in current:
            tempx = []
            tempy = []
            for ycol in ylist[index]:
                xt, yt = GetData(w.data,xlist[index]-1,ycol-1)
                tempx.append([xt,xlist[index]-1])
                tempy.append([yt,ycol-1])
            x.append(tempx[0])
            y.append(tempy)
        index += 1
        sheetindex = 0
        for xt in x:
            for yt in y[sheetindex]:
                tf = fitfunc(xt[0],yt[0])
                current[sheetindex].AddDatafit(tf,xt[1],yt[1])
            sheetindex += 1
    return True


def NonLinearFit(x,y,p0,func):
    coeff = []
    covarince = [[]]
    valid = False
    try:
        coeff,covarince = spo.curve_fit(func,x,y,p0=p0)
        valid = True
    except RuntimeError:
        coeff = p0
    
    return coeff, covarince, valid

def exponential_fit(x,y):
    exp_func = lambda x, a,b,c,d: a + b*np.exp(c*x + d)
    p0 = [0,1,-1,0]
    return_data = NonLinearFit(x,y,p0,exp_func)
    expfit = DataFit(exp_func, return_data[0], return_data[1])
    rsquared(expfit,x,y)
    return expfit

def fft(x,y):
    N = len(x)
    h = np.fft.fft(y,N)
    #PSD = h * np.conj/N
    #x_step = 0
    freq = np.fft.fftfreq(N)
    plotting.plt.plot(freq,h.real,freq,h.imag)
    plotting.plt.show()


def rsquared(curve : DataFit, x, y):
    r_sqaured_value = 0
    residuals = 0
    varience = 0
    sumy = sum(y)
    mean = sumy / len(y)
    curve.Eval(x)
    y_fit = curve.GetY()
    i = 0
    for y_val in y_fit:
        val = float(y[i]) - y_val
        residuals = residuals + math.pow(val,2)
        varience = varience + math.pow(y[i]-mean,2)
    r_sqaured_value = 1 - (residuals/varience)
    curve.add_r_sqaured(r_sqaured_value)
    return r_sqaured_value

