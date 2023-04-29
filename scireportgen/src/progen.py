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
    web.get_manual_of_week(get_last_week(), os.path.join(root, folder_name, "manual.pdf"))
    titles, aims = pdf.get_titles_and_aims(os.path.join(root, folder_name, "manual.pdf"))
    exp_cnt = len(titles)

def get_last_week() -> int:
    with open("data/last_week.data", "r") as f:
        res = int(f.readline())
    return res

def update_last_week(week:int) -> None:
    with open("misc/last_week.data", "w") as f:
        f.write(str(week))

if __name__ == "__main__":
    exp_day = input("날짜를 입력하시오. (YYYY-MM-DD) >>> ")
    make_proj_folder(os.getcwd(), exp_day)
