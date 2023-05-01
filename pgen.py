from scireportgen.src import progen
import os

if __name__ == "__main__":
    exp_day = input("날짜를 입력하시오. (YYYY-MM-DD) >>> ")
    progen.make_proj_folder(os.getcwd(), exp_day, progen.get_last_week())
    progen.update_last_week(progen.get_last_week() + 1)
