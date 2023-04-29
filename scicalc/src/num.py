"""Core of calculating scientific figures.

Typical usage example:

    pi = SuperFloat("3.1415926535", True)
    two = SuperFloat("2", True)
    2pi = two*pi

"""
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('log/my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def change_e_notation_2_LaTeX_notation(num_e_string:str) -> str: # pylint: disable=invalid-name
    """Change e notation to LaTeX notation.

    Args:
        num_e_string: a string represents float number using e notation.
    
    Returns:
        A string using LaTeX
    
    Raises:
        AssertionError: An error occurred if not e in num_e_string.
    """
    assert 'e' in num_e_string
    a, b = num_e_string.split('e')
    logger.info(f"change_e_notation_2_LaTeX_notation: {num_e_string=} {a=} {b=}")
    return f"{a}\\times 10^{{{b}}}"

def get_dot_index(num_string:str) -> int:
    """Get index of '.' in string.

    Args:
        num_string: a string represents float number.

    Returns:
        An integer. If '.' in num_string, return index of '.'. otherwise, return -1.

        For example: 1.12 -> 1. 1233 -> -1
    """
    for i, char in enumerate(num_string):
        if char == '.':
            return i
    return -1

def count_significant_figure(num_string:str, strict=False) -> int:
    """Count significant figures.

    If strict is True, trailing zeros without dot will not counted as significant figures.
    otherwise, It'll counted.

    Args:
        num_string: a string represents float number.
        strict: If True trailing zeros without dot will not counted as significant figures.

    Returns:
        An integer, count of significant figures.

    Raises:
        AssertionError: An error occured if num_string is empty.
    """
    logger.debug(f"Started count_significant_figure {num_string=} {strict=}")
    assert len(num_string) > 0

    i = 0 if num_string[0] != "-" else 1
    while (i < len(num_string)) and (num_string[i] == '0' or num_string[i] == '.'):
        i += 1
    dot_index = get_dot_index(num_string)

    k = 0
    if strict and dot_index == -1:
        while(num_string[-k -1] == '0'): k += 1
    res = len(num_string) - i - (1 if (dot_index > i) else 0) - k
    logger.debug(f"Finished count_significant_figure: {num_string=} {strict=} {i=} {k=} {dot_index=} {res=}")
    return res

def change_float_string_2_e_notation(num_string:str) -> str:
    """Change float string notation to e notation.

    Args:
        num_string: a string represent float number.

    Returns:
        A string represents float number with e notation.
    
    Raises:
        AssertionError: An error occured if num_string is empty.
    """
    logger.debug(f"Started change_float_string_2_e_notation {num_string=}")
    assert(len(num_string) > 0)
    dot_index = get_dot_index(num_string)

    is_minus = num_string[0] == '-'
    
    if dot_index == -1:
        if is_minus:
            logger.debug(f"Finished_1 change_float_string_2_e_notation {num_string[:2]=} {num_string[2:]} {len(num_string)-2=}")
            return f"{num_string[:2]}.{num_string[2:]}e{len(num_string)-2}"
        logger.debug(f"Finished_2 change_float_string_2_e_notation {num_string[0]=} {num_string[1:]} {len(num_string)-1=}")
        return f"{num_string[0]}.{num_string[1:]}e{len(num_string)-1}"

    if is_minus and dot_index == 2:
        i = 1
        while i < len(num_string) and (num_string[i] == '0' or num_string[i] == '.'): i += 1
        if i == 1:
            logger.debug(f"Finished_3 change_float_string_2_e_notation {num_string=}")
            return num_string
        logger.debug(f"Finished_4 change_float_string_2_e_notation {num_string[i]=} {num_string[i+1:]=} {2-i=}")
        return f"-{num_string[i]}.{num_string[i+1:]}e{2 - i}"

    if not is_minus and dot_index == 1:
        i = 0
        while i < len(num_string) and (num_string[i] == '0' or num_string[i] == '.'): i += 1
        if i == 0:
            logger.debug(f"Finished_5 change_float_string_2_e_notation {num_string=}")
            return num_string
        logger.debug(f"Finished_6_change_float_string_2_e_notation {num_string[i]=} {num_string[i+1:]=} {1-i=}")
        return f"{num_string[i]}.{num_string[i+1:]}e{1 - i}"

    if is_minus:
        logger.debug(f"Finished_7 change_float_string_2_e_notation {num_string[:2]=} {num_string[2:dot_index]=} {num_string[dot_index+1:]=} {dot_index-2=}")
        return f"{num_string[:2]}.{num_string[2:dot_index]}{num_string[dot_index+1:]}e{dot_index - 2}"
    logger.debug(f"Finished_8 change_float_string_2_e_notation {num_string[0]=} {num_string[1:dot_index]=} {num_string[dot_index+1:]=} {dot_index-1=}")
    return f"{num_string[0]}.{num_string[1:dot_index]}{num_string[dot_index+1:]}e{dot_index - 1}"

def cut_and_round(num_string:str, target:int|float) -> str:
    """Get most short prefix of num_string which has target significant figures.

    Args:
        num_string: a string represents float number.
        target: an integer or infinity. 

    Returns:
        A prefix of num_string which has target significant figures.
    
    Raises:
        AssertionsError: An error occured if significant figures of num_string is smaller than target.
    """
    if target != float('inf'):
        assert(count_significant_figure(num_string) >= target)

    if target == float('inf'): return num_string
    i = 1
    logger.debug(f"Started cut_and_round: {num_string=} {target=}")
    while i <= len(num_string):
        if target == count_significant_figure(num_string[:i]):
            if i == len(num_string):
                return num_string

            dot_index = get_dot_index(num_string)
            if dot_index == -1: dot_index = len(num_string)

            res = str(round(float(num_string[:i+1]), i - dot_index - 1))
            if i < dot_index:
                res = str(int(round(float(num_string[:i] + "." + num_string[i])))) + "0"*(dot_index - i)
            if i == dot_index:
                res = str(int(round(float(num_string[:i] + "." + num_string[i+1])))) + "0"*(dot_index - i)
            logger.debug(f"Finished cut_and_round: {num_string=} {target=} {dot_index=} {i=} {res=}")
            return res
        i += 1
    logger.error("Error: cut_and_round return NaN")
    return "NaN"

class SuperFloat:
    """enhanced version of float.

    Attributes:
        float:
        is_const:
        string:
        cnt_significant_figures:
        num_e_string:
    """

    def __init__(self, string:str, is_const:bool = False, target_cnt_significant_figures:int|float = -1) -> None:
        self.is_const = is_const

        if target_cnt_significant_figures == -1:
            self.string = string
        else: self.string = cut_and_round(string, target_cnt_significant_figures)
        
        if is_const:
            self.cnt_significant_figures = float('inf')
        else: self.cnt_significant_figures = count_significant_figure(self.string)

        self.float = float(self.string)
        if self.float == 0:
            self.num_e_string = "0"
        else:
            if is_const:
                self.num_e_string = self.string
            else:
                self.num_e_string = change_float_string_2_e_notation(self.string)
        logger.debug(f"SuperFloat constructed. {string=} {is_const=} {target_cnt_significant_figures=} {self.num_e_string=} {self.string=} {self.cnt_significant_figures=} {self.float=}")

    def __add__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(self.float + other.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError
        
    def __radd__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(self.float + other.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError
    
    def __mul__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(self.float * other.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError
        
    def __rmul__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(self.float * other.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError
    
    def __sub__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(self.float - other.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError

    def __rsub__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(other.float - self.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError
    
    def __truediv__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(self.float / other.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError

    def __rtruediv__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(other.float / self.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError
    
    def __floordiv__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(self.float // other.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError

    def __rfloordiv__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(other.float // self.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError
    
    def __mod__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(self.float % other.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError

    def __rmod__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(other.float % self.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError
    
    def __pow__(self, other):
        if isinstance(other, SuperFloat):
            return SuperFloat(str(self.float ** other.float), self.is_const and other.is_const, min(self.cnt_significant_figures, other.cnt_significant_figures))
        raise TypeError
    def __float__(self):
        return self.float
    
    def __int__(self):
        return int(self.float)
    
    def __str__(self):
        return self.string
    
    def __neg__(self):
        return SuperFloat(str(-self.float), self.is_const)
    
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