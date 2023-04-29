import typing
def make_textwidth_table_with_tabularx(table:typing.List[typing.List[typing.Any]], l_count:int = 1, caption:str = "", label:str = "") -> str:
    Y_count = len(table[0]) - l_count
    column = "|" + "l|"*l_count + "|Y"*Y_count + "|"
    content = ""
    for row in table:
        content += "        "
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

print(make_textwidth_table_with_tabularx([['it', 'val'], [1, 'a'], [2, 'b']]))