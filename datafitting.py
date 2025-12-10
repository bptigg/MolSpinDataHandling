import workspace
import scipy as sp
from scipy import optimize as spo
import numpy as np

def curvefit(agrs):
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
    return_data = NonLinearFit(x,y,exp_func,p0)

def rsquared():
    r_sqaured_value = 0
    return r_sqaured_value

