import typing
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "..")))

def make_textwidth_table_with_tabularx(table:typing.List[typing.List[typing.Any]], l_count:int = 1, caption:str = "", label:str = "") -> str:
    Y_count = len(table[0]) - l_count
    column = "|" + "c|"*l_count + "Y|"*Y_count
    content = ""
    for row in table:
        content += "    "
        for c in row:
            content += str(c) + " & "
        content = content[:-2]
        content += "\\\\ \\hline\n"
    content = content[:-1]
    return \
    f"""
\\begin{{table}}[H]
    \\begin{{tabularx}}{{\\textwidth}}{{{column}}}
    \\hline
    \\rowcolor{{Gray}}
{content}
    \\end{{tabularx}}
    \\caption{{{caption}}}\\label{{{label}}}
\\end{{table}}
    """

def make_textwidth_table_with_multirow(labels:typing.List[str], index_of_same_group:typing.List[typing.Tuple[int, int, str]], table_body:typing.List[typing.List[typing.Any]], l_count:int = 1, caption:str = "", label:str = "") -> str:
    Y_count = len(labels) - l_count
    column = "c"*l_count + "Y"*Y_count

    fisrt_line = ""
    i = 0
    j = 0
    second_line = ""
    flag = False
    while i <len(labels):
        if j < len(index_of_same_group):
            if index_of_same_group[j][0] <= i < index_of_same_group[j][1]:
                second_line += "\\Block{1-1}{\\centering " +labels[i] + "} & "
                flag = True
            elif i == index_of_same_group[j][1]:
                # assert flag

                flag = False
                fisrt_line += f"\\Block{{1-{index_of_same_group[j][1] - index_of_same_group[j][0] + 1}}}{{{index_of_same_group[j][2]}}} " + "& "*(index_of_same_group[j][1] - index_of_same_group[j][0] +1)
                j += 1
                second_line += "\\Block{1-1}{\\centering " +labels[i] + "} & "
            else:
                second_line += " & "
                fisrt_line += f"\\Block{{2-1}}{{{labels[i]}}} & "
        else:
            fisrt_line += f"\\Block{{2-1}}{{{labels[i]}}} & "
        i += 1
    if flag:
        fisrt_line += f"\\Block{{1-{index_of_same_group[j][1] - index_of_same_group[j][0]}}}{{{index_of_same_group[j][2]}}} & "

    body = ""
    for row in table_body:
        body += "        "
        for i in row:
            body += str(i) + " & "
        body = body[:-2] + "\\\\ \n"
    return \
    f"""
\\begin{{table}}[H]
    \\begin{{NiceTabularX}}{{\\textwidth}}{{{column}}}[hvlines, code-before=\\rectanglecolor{{Gray}}{{1-1}}{{2-{len(labels)}}}]
        
        \\toprule
        {fisrt_line[:-2]} \\\\
        {second_line[:-2]} \\\\

        \\midrule
{body}
    \\end{{NiceTabularX}}
    \\caption{{{caption}}}\\label{{{label}}}
\\end{{table}}
    """

if __name__ == "__main__":
    # print(make_textwidth_table_with_tabularx([['it', 'val'], [1, 'a'], [2, 'b']]))
    print(make_textwidth_table_with_multirow(["it", "t1", "t2"], [(1, 2, "time")], [[1, 2, 3], [2, 3, 4], [3, 2, 3]]))
    print(make_textwidth_table_with_multirow(["it", "t1", "t2", "a"], [(1, 2, "time")], [[1, 2, 3, 3], [2, 3, 4, 3], [3, 2, 3, 3]]))