import typing

def changeENot2LaTeXNot(string:str) -> str:
    a, b = string.split('e')
    return f"{a}\\times 10^{{{b}}}"

def getDotIndex(string:str) -> int:
    for j in range(len(string)):
        if string[j] == '.':
            return j
    return -1

def countSigFig(numString:str) -> int:
    assert(len(numString) > 0)

    i = 0 if numString[0] != "-" else 1
    while (i < len(numString)) and (numString[i] == '0' or numString[i] == '.'): i += 1
    dotIndex = getDotIndex(numString)

    j = 0
    while (j < len(numString)) and (numString[-j-1] == '0'): j += 1
    return len(numString) - i - (1 if (dotIndex > i) else 0) - (j if dotIndex == -1 else 0)

def changeFloatStr2SciNot(numString:str) -> str:
    assert(len(numString) > 0)
    dotIndex = getDotIndex(numString)

    isMinus = numString[0] == '-'
    
    if dotIndex == -1:
        if isMinus: return f"{numString[:2]}.{numString[2:]}e{len(numString)-2}"
        else: return f"{numString[0]}.{numString[1:]}e{len(numString)-1}"
    elif isMinus and dotIndex == 2:
        i = 1
        while i < len(numString) and (numString[i] == '0' or numString[i] == '.'): i += 1
        if i == 0:
            return numString
        else:
            return f"-{numString[i]}.{numString[i+1:]}e{2 - i}"
    elif not isMinus and dotIndex == 1:
        i = 0
        while i < len(numString) and (numString[i] == '0' or numString[i] == '.'): i += 1
        if i == 0:
            return numString
        else:
            return f"-{numString[i]}.{numString[i+1:]}e{1 - i}"
    else:
        if isMinus: return f"{numString[:2]}.{numString[2:dotIndex]}{numString[dotIndex+1:]}e{dotIndex - 2}"
        else: return f"{numString[0]}.{numString[1:dotIndex]}{numString[dotIndex+1:]}e{dotIndex - 1}"

def cutAndRound(numString:str, target:int|float) -> str:
    assert(countSigFig(numString) >= target)

    if target == float('inf'): return numString
    i = 1
    while i <= len(numString):
        if target == countSigFig(numString[:i]):
            if i == len(numString): return numString
            else:
                dotIndex = getDotIndex(numString)
                if dotIndex == -1: dotIndex = len(numString)

                if i <= dotIndex: return str(int(round(float(numString[:i] + "." + numString[i])))) + "0"*(dotIndex - i)
                else: return str(round(float(numString[:i+1]), i - dotIndex - 1))
        i += 1
    return "NaN"

class NumSig:
    isConst, string, sigCnt, sciNotString = False, "", -1, ""

    def __init__(self, string:str, isConst:bool = False, targetSigFig:int|float = -1) -> None:
        self.isConst = isConst

        if targetSigFig == -1: self.string = string
        else: self.string = cutAndRound(string, targetSigFig)
        
        if isConst: self.sigCnt = float('inf')
        else: self.sigCnt = countSigFig(self.string)

        self.float = float(self.string)
        if self.float == 0:
            self.sciNotString = "0"
        else:
            if isConst: self.sciNotString = self.string
            else: self.sciNotString = changeFloatStr2SciNot(self.string)

    def __add__(self, other):
        if type(other) == NumSig: return NumSig(str(self.float + other.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))
        
    def __radd__(self, other):
        if type(other) == NumSig: return NumSig(str(self.float + other.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))
    
    def __mul__(self, other):
        if type(other) == NumSig: return NumSig(str(self.float * other.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))
        
    def __rmul__(self, other):
        if type(other) == NumSig: return NumSig(str(self.float * other.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))
    
    def __sub__(self, other):
        if type(other) == NumSig: return NumSig(str(self.float - other.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))

    def __rsub__(self, other):
        if type(other) == NumSig: return NumSig(str(other.float - self.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))
    
    def __truediv__(self, other):
        if type(other) == NumSig: return NumSig(str(self.float / other.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))

    def __rtruediv__(self, other):
        if type(other) == NumSig: return NumSig(str(other.float / self.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))
    
    def __floordiv__(self, other):
        if type(other) == NumSig: return NumSig(str(self.float // other.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))

    def __rfloordiv__(self, other):
        if type(other) == NumSig: return NumSig(str(other.float // self.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))
    
    def __mod__(self, other):
        if type(other) == NumSig: return NumSig(str(self.float % other.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))

    def __rmod__(self, other):
        if type(other) == NumSig: return NumSig(str(other.float % self.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))
    
    def __pow__(self, other):
        if type(other) == NumSig: return NumSig(str(self.float ** other.float), self.isConst and other.isConst, min(self.sigCnt, other.sigCnt))
    def __float__(self):
        return self.float
    
    def __int__(self):
        return int(self.float)
    
    def __str__(self):
        return self.sciNotString
    
    def __neg__(self):
        return NumSig(str(-self.float), self.isConst)
    
    def __pos__(self):
        return self
    
    def __lt__(self, other):
        return self.float < other.float
    
    def __le__(self, other):
        return self.float <= other.float
    
    def __gt__(self, other):
        return self.float > other.float
    
    def __ge__(self, other):
        return self.float >= other.float
    
    def __eq__(self, other):
        return self.float == other.float
    
    def __ne__(self, other):
        return self.float != other.float