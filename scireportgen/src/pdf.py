import re
import typing

import pdftotext

exp_title_pattern = re.compile(r"실험\d+-{0,1}\d?\.?.+")
aim_pattern = re.compile(r"1 ?\. ?목 ?적.+2 ?\.", re.DOTALL)

def get_titles_and_aims(pdf_name:str) -> typing.Tuple[typing.List[str], typing.List[str]]:
    with open(pdf_name, "rb") as f:
        f_reader = pdftotext.PDF(f)
        titles = []
        aims = []
        for raw_page in f_reader:
            page = raw_page.replace(" ", "")
            title = exp_title_pattern.search(page)
            if title is not None:
                title = title.group().split('.')[-1]
                titles.append(title)

            aim = aim_pattern.search(raw_page)
            if aim is not None:
                aim = aim.group()
                i = 0
                while aim[i] != '\n': i += 1
                aim = aim[i+1:]
                j = 1
                while aim[-j] in ['.', '\n'] + [chr(ord('0') + i) for i in range(10)]: j += 1
                aim = aim[:-j+1]
                aim = aim.replace("\n", "")
                aim = aim.replace(". ", ".")
                aim = aim.replace(", ", ",")
                aim = aim.replace(".", ".\n")
                aim = aim.replace(",", ",\n")
                aims.append(aim)
    if len(aims) != len(titles):
        print(aims)
        indexes = [int(i) for i in input("aims 에서 남기고 싶은 인덱스를 스페이스로 구분해서 입력하세요 >>>").split()]
        aims = [aims[i] for i in indexes]
        print(titles)
        indexes = [int(i) for i in input("titles 에서 남기고 싶은 인덱스를 스페이스로 구분해서 입력하세요 >>>").split()]
        titles = [titles[i] for i in indexes]

    return titles, aims
    
if __name__ == "__main__":
    titles, aims = get_titles_and_aims('asdf.pdf')
    print(titles, aims)