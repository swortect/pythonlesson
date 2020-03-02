import os
import re
import requests
from bs4 import BeautifulSoup as bs
myurl = "https://docs.python.org/zh-cn/3.7/"
pages=[]
def getPage(url):
    global myurl
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    header = {}
    header['user-agent'] = user_agent
    response = requests.get(url, headers=header)
    print(response.apparent_encoding)
    bs_info = bs(response.text, 'lxml')
    pages=[str(myurl+x.get("href")) for x in bs_info.find_all('a') if x.get("href")[-5:]=='.html']
    link = [str(myurl+x.get("href")) for x in bs_info.find_all('link') if x.get("href")[-4:]=='.css']
    script = [str(myurl+x.get("src")) for x in bs_info.find_all('script') if x.get("src") is not None]
    if(url==myurl):
        pages.append(myurl+'index.html')
    pages.reverse()
    print(pages)
    if (len(pages)>0):
        for i in pages:
            path=re.sub("https://docs.python.org/zh-cn/","",i)
            print(i)
            dir=re.sub(os.path.basename(path),"",path)
            if not os.path.exists(dir):
                os.makedirs(dir)
            response2 = requests.get(i, headers=header)
            encoding=response2.apparent_encoding
            print(encoding)
            with open(path, 'w+',encoding='utf-8') as f:
                f.write(response2.content.decode('utf-8'))
            #getPage(i)
getPage(myurl)