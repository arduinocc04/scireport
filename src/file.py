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
from src import num

CMD = "@@"
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('log/my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def find_cmd(string:str, cmd:str) -> typing.List[int]:
    ans = []
    for i in range(len(string) - len(cmd) + 1):
        flag = True
        for j in range(len(cmd)):
            if string[i + j] != cmd[j]:
                flag = False
                break
        if flag:
            ans.append(i)
    logger.debug(f"find_cmd: {string=} {cmd=} {ans=}")
    return ans

numList = [chr(ord('0') + i) for i in range(10)] + ["_", "{", "}", "!", "."]

def change_expression_num_str_2_SuperFloat_str(expression_num:str) -> str:
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

    logger.debug(f"change_expression_num_str_2_SuperFloat_str: {expression_num=} {is_const=} {sig_fig_target=}")
    if sig_fig_target == -1:
        return f"num.SuperFloat('{expression_num}', {is_const})"
    return f"num.SuperFloat('{expression_num}', {is_const}, {sig_fig_target})"

def change_expression(expression:str) -> str:
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
                resExpression += change_expression_num_str_2_SuperFloat_str(num) + expression[i]

            else:
                resExpression += expression[i]
        i += 1
    if flag:
        resExpression += change_expression_num_str_2_SuperFloat_str(expression[prev:])
    logger.debug(f"change_expression: {expression=} {resExpression=}")
    return resExpression

def change_line(line:str, cmd:str) -> str:
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
        logger.debug(f"change_line: {expression=} {str(res)=}")
    res_line += line[prev:]
    return res_line

def change_file(inputFileName, outputFileName):
    inputFile = open(inputFileName, "r")
    outputFile = open(outputFileName, "w")

    for line in inputFile:
        outputFile.write(change_line(line, CMD))

    inputFile.close()
    assert inputFile.closed
    outputFile.close()
    assert outputFile.closed