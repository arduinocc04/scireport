import os
import bs4

url="https://physlab.sogang.ac.kr/bbs/bbslist.do?forword=&wslID=physlab&bbsid=2089"

def make_proj_folder(root:str, folder_name:str) -> None:
    os.mkdir(os.path.join(root, folder_name))
    os.mkdir(os.path.join(root, folder_name, "Data"))
    os.mkdir(os.path.join(root, folder_name, "tex"))
    os.mkdir(os.path.join(root, folder_name, "tex", "img"))

def get_last_week() -> int:
    with open("data/last_week.data", "r") as f:
        res = int(f.readline())
    return res

def update_last_week(week:int) -> None:
    with open("data/last_week.data", "w") as f:
        f.write(str(week))
    


if __name__ == "__main__":
    exp_day = input("날짜를 입력하시오. (YYYY-MM-DD) >>> ")
    make_proj_folder(os.getcwd(), exp_day)
