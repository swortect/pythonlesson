import requests
from bs4 import BeautifulSoup as bs
import re
import csv
from time import sleep
from fake_useragent import UserAgent
import time

#调试
def z(data):
    print(data)
    exit()

#统一http请求
def getHttp(url):
    ua = UserAgent()
    headers = {
        'User-Agent':  ua.random
    }
    print(ua.random)
    res = requests.get(url, headers=headers, timeout=(3,7))
    if (res.status_code==200):
        html = res.text.encode('iso-8859-1')

        return bs(html, 'lxml')
    else:
        return False

def maker(url):
    last_img = 'http://p.ggrrtt.com/uploadfile/2016/0918/08/173.jpg'
    result = re.search('/(.+?\.jpg)', last_img)
    z(result[1])
    bs_info = getHttp(url)

    title=bs_info.find('div',{'class':'content_title'}).text
    pages = [x for x in bs_info.find_all('a', {'class': 'a1'})]
    last_url=pages[1].previous_sibling.previous_sibling.get('href')
    last_page = getHttp('http://www.ggrrtt.com'+last_url)
    img=[x for x in last_page.find_all('img')]
    last_img=img[-1].get('src')


urls="http://www.ggrrtt.com/html/yazhou/2016/0918/4532.html"

if __name__ == '__main__':
    maker(urls)