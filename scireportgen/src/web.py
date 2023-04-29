from bs4 import BeautifulSoup
import requests

url="https://physlab.sogang.ac.kr/bbs/bbslist.do?forword=&wslID=physlab&bbsid=2089"

def get_manual_of_week(week:int, download_location:str):
    html = requests.get(url, verify="misc/sogang-ac-kr-chain.pem").text
    bs_object = BeautifulSoup(html, "lxml")
    trs = bs_object.find_all("tr")
    
    target_tr = None
    for tr in trs:
        tmp = tr.find("td")
        if tmp is None: continue
        if tmp.text == str(week):
            target_tr = tr
            break
    
    if target_tr is None:
        raise FileNotFoundError
    
    kor = ['한', 'kor', '국', '어']
    manual_download_as = target_tr.find_all("a")
    
    res = None
    for a in manual_download_as:
        href = a.get('href')
        for k in kor:
            if k in href.lower():
                res = "https://physlab.sogang.ac.kr" + href
                break
        if res is not None: break

    if res is None:
        raise ModuleNotFoundError

    file = requests.get(res, verify="misc/sogang-ac-kr-chain.pem")
    with open(download_location, "wb") as f:
        f.write(file.content)

if __name__ == "__main__":
    get_manual_of_week(2, "asdf.pdf")