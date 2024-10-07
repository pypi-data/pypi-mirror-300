#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Current version 1.3 (Using a trail to undo a search)
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2023
#
# Modules:
#   PythonCPSolver
#       engine.py
#       propagators.py
#       variables.py
#       brancher.py
#====================================================================

from .variables import *

#====================================================================

class Propagator :
    def __init__(self) -> None:
        pass

    #--------------------------------------------------------------
    def __str__(self) -> str:
        return self.toStr()

    #--------------------------------------------------------------
    def setEngine(self, engine) :
        pass

#====================================================================

class AllDifferent(Propagator) :
    def __init__(self, vars:list) -> None:
        Propagator.__init__(self, )
        self.vars = vars

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return 'alldifferent('+toStrs(self.vars ,printview)+')'

    #--------------------------------------------------------------
    def prune(self) :
        for v1 in self.vars :
            if v1.isAssigned() :
                for v2 in self.vars :
                    if id(v1) != id(v2) :
                        if v1.min == v2.min :
                            if not v2.project(
                                v2.min+1, 
                                v2.max ) : return False
                        if v1.max == v2.max :
                            if not v2.project(
                                v2.min, 
                                v2.max-1 ) : return False
        return True

#====================================================================

class Linear(Propagator) :
    def __init__(self, vars, vart) -> None:
        if isinstance(vart, int) : vart = IntVar(vart,vart)
        self.vars   = vars
        self.vart   = vart

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return str(self.vars)+' = '+str(self.valt)
    
    #--------------------------------------------------------------
    def prune(self) :
        maxs, mins = 0, 0
        for v in self.vars :
            maxs += v.max
            mins += v.min
        if not self.vart.project( mins, maxs ) : return False

        for v1 in self.vars :
            maxs, mins = 0, 0
            for v2 in self.vars :
                if id(v1) != id(v2) :
                    maxs += v2.max
                    mins += v2.min
            if not v1.project(
                self.vart.min-maxs, 
                self.vart.max-mins ) : return False
        return True

#====================================================================

class LinearArgs(Propagator) :
    def __init__(self, args, vars, vart) -> None:
        if isinstance(vart, int) : vart = IntVar(vart,vart)
        self.args   = args
        self.vars   = vars
        self.vart   = vart

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return str(self.vars)+' = '+str(self.valt)
    
    #--------------------------------------------------------------
    def prune(self) :
        maxs, mins = 0, 0
        for i,v in enumerate(self.vars) :
            if self.args[i] >= 0 :
                maxs += v.max * self.args[i]
                mins += v.min * self.args[i]
            else :
                maxs += v.min * self.args[i]
                mins += v.max * self.args[i]

        if not self.vart.project( mins, maxs ) : return False

        for i1,v1 in enumerate(self.vars) :
            maxs, mins = 0, 0
            for i2,v2 in enumerate(self.vars) :
                if id(v1) != id(v2) :
                    if (self.args[i1] >= 0 and self.args[i2] >= 0) or \
                       (self.args[i1]  < 0 and self.args[i2] < 0):                        
                        maxs += v2.max * self.args[i2]
                        mins += v2.min * self.args[i2]
                    else :
                        maxs += v2.min * self.args[i2]
                        mins += v2.max * self.args[i2]
            if self.args[i1] >= 0 :
                if not v1.project(
                    math.floor((self.vart.min - maxs)/self.args[i1]), 
                    math.ceil ((self.vart.max - mins)/self.args[i1])) : return False
            else :
                if not v1.project(
                    math.floor((mins - self.vart.max)/(self.args[i1]*-1)), 
                    math.ceil ((maxs - self.vart.min)/(self.args[i1]*-1))) : return False

        return True

#====================================================================
    
class Constraint(Propagator) :
    def __init__(self, exp:Expression) -> None:
        self.exp = exp

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return self.exp.toStr(printview)
    
    #--------------------------------------------------------------
    def prune(self) :
        self.exp.evaluate()
        return self.exp.project(1,1)
    
    #--------------------------------------------------------------
    def match(self, localvars:list, globalvars:list) :
        return Constraint( self.exp.match(localvars, globalvars) )

    #--------------------------------------------------------------
    def setEngine(self, engine) :
        self.exp.setEngine(engine)

#====================================================================

def count(vars:list, cond:Expression) -> Expression:
    exp = vars[0]==cond
    for i in range(1,len(vars)):
        exp = exp + (vars[i]==cond)
    return exp

#--------------------------------------------------------------

def alldifferent(vars:list) -> Expression:
    exp = vars[0] if len(vars)==1 else None
    for i in range(len(vars)-1):
        for j in range(i+1,len(vars)):
            if exp is None :
                exp = (vars[i] != vars[j])
            else :
                exp = exp & (vars[i] != vars[j])

    return exp

#--------------------------------------------------------------
def clause(vars:list, vals:list) -> Expression:
    exp = (vars[0] != vals[0]) if len(vars)==1 else None
    for i in range(len(vars)):
        if exp is None :
            exp = (vars[i] != vals[i])
        else :
            exp = exp | (vars[i] != vals[i])

    return exp

#--------------------------------------------------------------

def sum(vars:list) -> Expression:
    exp = vars[0]
    for i in range(1,len(vars)):
        exp = exp + vars[i]
    return exp
