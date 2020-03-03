from threading import Thread,current_thread
import time
import random
from queue import Queue
import os
import re
import requests
from bs4 import BeautifulSoup as bs
myurl = "https://docs.python.org/zh-cn/3.7/"

queue = Queue(1000)
queue2 = Queue(5)
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
header = {}
header['user-agent'] = user_agent

queue2.put(myurl)
queue2.put("https://docs.python.org/zh-cn/3.7/library/")
queue2.put("https://docs.python.org/zh-cn/3.7/reference/")
queue2.put("https://docs.python.org/zh-cn/3.7/tutorial/")

def spider(url):

    response = requests.get(url, headers=header)
    print(response.apparent_encoding)
    bs_info = bs(response.text, 'lxml')
    pages = [str(url + x.get("href")) for x in bs_info.find_all('a') if x.get("href")[-5:] == '.html']
    pages.append(url + 'index.html')
    link = [str(url + x.get("href")) for x in bs_info.find_all('link') if x.get("href")[-4:] == '.css']
    pages = pages + link
    script = [str(url + x.get("src")) for x in bs_info.find_all('script') if x.get("src") is not None]
    pages = pages + script
    return pages
def save(i):
    path = re.sub("https://docs.python.org/zh-cn/", "", i)
    print(i)
    dir = re.sub(os.path.basename(path), "", path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    response2 = requests.get(i, headers=header)
    encoding = response2.apparent_encoding
    print(encoding)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(response2.content.decode('utf-8'))
class ProducerThread(Thread):

    def run(self):
        name = current_thread().getName()
        global queue
        while True:
            urls = queue2.get()
            print(urls)
            queue2.task_done()
            for i in spider(urls):
                queue.put(i)
                print(f'入列{i}')


class ConsumerTheard(Thread):
    def run(self):
        name = current_thread().getName()
        global queue
        while True:

            url = queue.get()
            save(url)
            queue.task_done()
            print(queue.qsize())
            print(f'出列{url}')
p1 = ProducerThread(name = 'p1')
p1.start()
c1 = ConsumerTheard(name = 'c1')
c1.start()
c2 = ConsumerTheard(name = 'c2')
c2.start()
c3 = ConsumerTheard(name = 'c3')
c3.start()