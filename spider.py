import csv
import functools
import re
from multiprocessing.dummy import Pool,Manager

import requests
from bs4 import BeautifulSoup

from config import *
def get_index(lock,page):
    if page==1:
        url= START_URL+'pg' + str(0)
    else:
        url=START_URL+'pg'+str(page)
    headers = {"Accept-Language": "zh-CN,zh;q=0.9","User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    try:
        res=requests.get(url,headers=headers)
        res.encoding = 'utf-8'
        parse_index(lock,res.text)
    except ConnectionError:
        print('connect again')
        return None

def parse_index(lock,html):
    home_list=[]
    bsobj = BeautifulSoup(html, "html5lib")
    homeList=bsobj.find_all("div", {"class":"info clear"})
    for homeInfo in homeList:
        title = homeInfo.find("div", {"class": "title"}).get_text()
        info = homeInfo.find("div", {"class": "houseInfo"}).get_text().split("/")
        block=info[0].strip()
        home_type=info[1].strip()
        home_area=info[2].strip()
        home_area=re.findall('\d+',home_area)[0]
        detail=','.join(info[3:])
        price=homeInfo.find('div',{'class':'totalPrice'}).span.get_text()
        price=re.findall('\d+',price)[0]
        home_list.append({
            'title':title,
            'block':block,
            'home_type':home_type,
            'home_area':home_area,
            'price':price,
            'detail':detail
        })
    save_csv(lock,home_list)

def save_csv(lock,home_list):
    with open('house.csv','a',encoding='utf-8') as f:
        writer=csv.writer(f)
        # writer.writerow(['title','block','home_type','home_area','price','detail'])
        for home_dict in home_list:
            lock.acquire()
            writer.writerow(home_dict.values())
            lock.release()

def main():
    manager=Manager()
    lock=manager.Lock()
    partial_get_index=functools.partial(get_index,lock)
    pool=Pool()
    pool.map(partial_get_index,[i for i  in range(START_PAGE,END_PAGE+1)])
    pool.close()
    pool.join()
    print('over')


if __name__=='__main__':
    main()