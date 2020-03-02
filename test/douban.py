import requests
from bs4 import BeautifulSoup as bs
import re
import csv
from time import sleep
from fake_useragent import UserAgent

#统一http请求
def getHttp(url):
    ua = UserAgent()
    headers = {
        'User-Agent':  ua.random
    }
    print(ua.random)
    res = requests.get(url, headers=headers)
    if (res.status_code==200):
        return bs(res.text, 'lxml')
    else:
        return False

def getComment(url):
    bs_info=getHttp(url+'comments/hot?p=1')
    comment=[x.text for x in bs_info.find_all('span',{'class':'short'}, limit=5)]
    return comment
def maker(url):
    global num
    bs_info = getHttp(url)
    title=[re.sub(' ','',x.text).strip('\n') for x in bs_info.find_all('div',{'class':'pl2'})]
    title=[re.sub('\n','',x) for x in title]
    href=[x.find('a').get('href') for x in bs_info.find_all('div',{'class':'pl2'})]
    star=[x.text for x in bs_info.find_all('span',{'class':'rating_nums'})]
    comment_num=[re.sub(' ','',x.text)[2:-5] for x in bs_info.find_all('span',{'class':'pl'})]
    print('列表读取完毕')
    sum= []
    for i in range(0,25):
        comment_top5=getComment(href[i])
        print(f'{num}、{title[i]}评论读取完毕')
        #sleep(1)
        sum.append([title[i],star[i],comment_num[i],
                    comment_top5[0],
                    comment_top5[1],
                    comment_top5[2],
                    comment_top5[3],
                    comment_top5[4]])
        num+=1
    return sum

urls=tuple([f'https://book.douban.com/top250?start={str(x)}' for x in range(0,226,25)])

if __name__ == '__main__':

    num = 1
    data=[]
    #for page in urls:
    page=urls[0]
    data=data+maker(page)

    with open("douban250" + ".csv", "w+", newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['书名', '评分', '短评数量','评论1','评论2','评论3','评论4','评论5'])
        for i in data:
            writer.writerow(i)
        print('csv写入完毕')