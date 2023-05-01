"""
Usage:
    Wrap expression you want to calculate with "@@".
    If you want to mark is_const, mark "!" in front of number. White space isn't allowed.
    If you want to set cnt_significant_figures, append _{num} to number. white space isn't allowed.
Example:
    1.32 + 2.34 = @@1.32 + 2.34@@
    a is 1231. double of a is @@!2 * 1231.@@
    @@123.123123123123112_{1}@@
"""
import typing
import logging
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "..")))
from src import num
from scireportgen.src.latex_helper import make_textwidth_table_with_tabularx
from scireportgen.src.latex_helper import make_textwidth_table_with_multirow
CMD = "@@"
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), '..', "..", "log", "my.log"))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def find_cmd(string:str, cmd:str) -> typing.List[int]:
    """Return start indexes of cmd in string.

    Args:
        string: a string.
        cmd: a string..
    
    Returns:
        A array contains indexes of cmd in string.
    """
    logger.debug(f"Started find_cmd: {string=} {cmd=}")
    ans = []
    for i in range(len(string) - len(cmd) + 1):
        flag = True
        for j in range(len(cmd)):
            if string[i + j] != cmd[j]:
                flag = False
                break
        if flag:
            ans.append(i)
    logger.debug(f"Finished find_cmd: {string=} {cmd=} {ans=}")
    return ans

numList = [chr(ord('0') + i) for i in range(10)] + ["_", "{", "}", "!", ".", "-"]

def change_float_string_2_SuperFloat_str(expression_num:str) -> str:
    """Change float string to SuperFloat constructor string.

    Args:
        expression_num: a string consists of number or expression mark or underbar, or brace or dot.
    
    Returns:
        A string that can construct SuperFloat Object in eval.
    """
    logger.debug(f"Started change_float_string_2_SuperFloat_str: {expression_num=}")
    is_const = False
    if expression_num[0] == "!":
        is_const = True
        expression_num = expression_num[1:]
    sig_fig_target = -1
    if expression_num[-1] == "}":
        i = 0
        while(expression_num[-i -1] != "_"):
            i += 1

        sig_fig_target = int(expression_num[-i +1:-1])
        expression_num = expression_num[:-i - 1]
        logger.debug(f"{i=}")

    logger.debug(f"Finished change_float_string_2_SuperFloat_str: {expression_num=} {is_const=} {sig_fig_target=}")
    if sig_fig_target == -1:
        return f"num.SuperFloat('{expression_num}', {is_const})"
    return f"num.SuperFloat('{expression_num}', {is_const}, {sig_fig_target})"

def change_expression(expression:str) -> str:
    """Change an equation consists of float strings and operators to SuperFloat constructor strings and same operators.

    Args:
        expression: a string which represents an equation consists of float strings and operators.

    Returns:
        a string consists of SuperFloat constructors and operators which  is ideal to given expression.
    """
    logger.debug(f"Started change_expression: {expression=}")
    resExpression = ""
    i = 0
    prev = 0
    flag = False
    while i < len(expression):
        if expression[i] in numList:
            if flag:
                pass
            else:
                flag = True
                prev = i
        else:
            if flag:
                flag = False
                num = expression[prev:i]
                resExpression += change_float_string_2_SuperFloat_str(num) + expression[i]

            else:
                resExpression += expression[i]
        i += 1
    if flag:
        resExpression += change_float_string_2_SuperFloat_str(expression[prev:])
    logger.debug(f"Finished change_expression: {expression=} {resExpression=}")
    return resExpression

def execute_python_code(line:str, cmd='!!') -> None:
    logger.debug(f"Started execute_python_code {line=} {cmd=}")
    tmp = find_cmd(line, cmd)
    if len(tmp) == 0: return
    idx = tmp[0]
    exec(line[idx+2:].lstrip())
    logger.debug(f"Finished execute_python_code {line=} {cmd=} {line[idx+2:]=} {idx=}")

def change_line(line:str, cmd:str) -> str:
    """Calculate expression surrounded by cmd.

    Args:
        line: A string that may contain expression surrounded by cmd
        cmd: A marker surround expression.
    
    Returns:
        a string that calculated expression in given line.
    """
    logger.debug(f"Started change_line: {line=} {cmd=}")
    idxs = find_cmd(line, cmd)
    if len(idxs) == 0:
        return line

    assert len(idxs) % 2 == 0

    res_line = ""
    cnt = len(idxs)//2
    prev = 0
    for i in range(cnt):
        res_line += line[prev:idxs[2*i]]
        expression = line[idxs[2*i] + 2:idxs[2*i + 1]]
        res = eval(change_expression(expression))
        res_line += str(res)
        prev = idxs[2*i + 1]+2
        logger.debug(f"Running change_line: {expression=} {str(res)=}")
    res_line += line[prev:]
    logger.debug(f"Finished change_line: {line=}")
    return res_line

def change_file(input_file_name:str, output_file_name:str, cmd:str) -> None:
    """Calculate expression surrounded by cmd.
    
    Args:
        input_file_name: a string 
        output_file_name: a string
        cmd: a string surrounds expression.

    Returns:
        None
    """
    logger.debug(f"Started change_file: {input_file_name=} {output_file_name=} {cmd=}")
    input_file = open(input_file_name, "r")
    output_file = open(output_file_name, "w")

    for line in input_file.readlines():
        output_file.write(change_line(line, cmd))

    input_file.close()
    assert input_file.closed
    output_file.close()
    assert output_file.closed
    logger.debug(f"Finished change_file: {input_file_name=} {output_file_name=}")

def change_and_execute_line(line:str) -> str:
    tmp = change_line(line, CMD)
    execute_python_code(tmp)
    return tmp

def change_and_execute_file(input_file_name:str, output_file_name:str, cmd:str) -> None:
    logger.debug(f"Started change_file: {input_file_name=} {output_file_name=} {cmd=}")
    input_file = open(input_file_name, "r")
    output_file = open(output_file_name, "w")

    for line in input_file.readlines():
        tmp = change_line(line, cmd)
        execute_python_code(tmp)
        output_file.write(tmp)

    input_file.close()
    assert input_file.closed
    output_file.close()
    assert output_file.closed
    logger.debug(f"Finished change_file: {input_file_name=} {output_file_name=}")