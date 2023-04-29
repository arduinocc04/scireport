import typing
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import web
from src import pdf

def make_proj_folder(root:str, folder_name:str) -> None:
    """
    /manual.pdf
    /Data
    /tex/ex{i}/
    /tex/main.tex
    /tex/img/
    """
    os.mkdir(os.path.join(root, folder_name))
    os.mkdir(os.path.join(root, folder_name, "Data"))
    os.mkdir(os.path.join(root, folder_name, "tex"))
    os.mkdir(os.path.join(root, folder_name, "tex", "img"))
    title = web.get_manual_of_week(get_last_week(), os.path.join(root, folder_name, "manual.pdf"))
    titles, aims = pdf.get_titles_and_aims(os.path.join(root, folder_name, "manual.pdf"))
    exp_cnt = len(titles)
    for i in range(1, exp_cnt + 1):
        os.mkdir(os.path.join(root, folder_name, "tex", f"ex{i}"))
        with open(os.path.join(root, folder_name, "tex", f"ex{i}", f"ex{i}.tex"), "w") as f:
            with open("scireportgen/data/ex_template.tex", "r") as g:
                template = g.readlines()
            for j in range(len(template)):
                template[j] = template[j].replace("!!aim!!", aims[i-1]).replace("!!num!!", str(i))
            for line in template:
                f.write(line)
        f = open(os.path.join(root, folder_name, "tex", f"ex{i}", f"ex{i}Data.tex"), "w")
        f.close()
        f = open(os.path.join(root, folder_name, "tex", f"ex{i}", f"ex{i}Analyze.tex"), "w")
        f.close()
        f = open(os.path.join(root, folder_name, "tex", f"ex{i}", f"ex{i}Question.tex"), "w")
        f.close()
        with open(os.path.join(root, folder_name, "tex", f"ex{i}", f"ex{i}Discussion.tex"), "w") as f:
            with open("scireportgen/data/exDiscussion_template.tex", "r") as g:
                template = g.readlines()
            for line in template:
                f.write(line)
    with open(os.path.join(root, folder_name, "tex", "main.tex"), 'w') as f:
        with open("scireportgen/data/main_template.tex", "r") as g:
            template = g.readlines()
        
        with open("misc/author.data", "r") as g:
            author = g.readline().rstrip()

        chapters = ""
        for i in range(len(titles)):
            chapters += f"\\chapter{{{titles[i]}}}\n    \\input{{ex{i+1}/ex{i+1}.tex}}\n"

        for i in range(len(template)):
            template[i] = template[i].replace("!!AUTHOR!!", author).replace("!!TITLE!!", title).replace("!!CHAPTERS!!", chapters)
        for line in template:
            f.write(line)

def get_last_week() -> int:
    with open("misc/last_week.data", "r") as f:
        res = int(f.readline())
    return res

def update_last_week(week:int) -> None:
    with open("misc/last_week.data", "w") as f:
        f.write(str(week))

if __name__ == "__main__":
    exp_day = input("날짜를 입력하시오. (YYYY-MM-DD) >>> ")
    make_proj_folder(os.getcwd(), exp_day)
