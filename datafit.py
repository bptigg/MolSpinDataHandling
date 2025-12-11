from enum import Enum

class FitType(Enum):
    LINEAR = 0
    EXP = 1
    LOGARITHMIC = 2
    GUASSIAN = 3


class DataFit:
    def __init__(self, evalfunc, coeff, covarience):
        self.func = evalfunc
        self.param = coeff
        self.covarience = covarience
        self.r_sqaured = 0
        self.data_x = []
        self.data_y = []
        pass

    def Copy(self, f2 : DataFit):
        self.func = f2.func
        self.param = f2.param
        self.covarience = f2.covarience
        self.r_sqaured = f2.r_sqaured
        self.data_x = f2.data_x
        self.data_y = f2.data_y

    def Eval(self, x : list):
        self.data_x = x
        y = [] 
        for i in x:
            val = self.func(i,*self.param)
            y.append(val)
        self.data_y = y
    
    def add_r_sqaured(self, rs):
        self.r_sqaured = rs

    def GetX(self):
        return self.data_x

    def GetY(self):
        return self.data_y
    
    def GetXY(self):
        return self.data_x, self.data_y


