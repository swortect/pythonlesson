import requests
from bs4 import BeautifulSoup as bs
from threading import Thread, current_thread,active_count
from queue import Queue
import re
import csv
from time import sleep
from fake_useragent import UserAgent
import time

# 由于多并发读取，统一由写入队列消费，不能保证顺序，所以多读一个排名字段，供业务使用


class Douban():
    def __init__(self):
        pass

    def getHttp(self, url):
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random
        }
        # print(ua.random)
        res = requests.get(url, headers=headers)
        if (res.status_code == 200):
            return bs(res.text, 'lxml')
        else:
            print("error")
            return False

    def getComment(self, url):
        bs_info = self.getHttp(url + 'comments?sort=new_score&status=P')
        comment = [re.sub(r'\s+', '', x.text) for x in bs_info.find_all(
            'span', {'class': 'short'}, limit=5)]
        return comment

    def maker(self, url):
        # global num
        print(url)
        bs_info = self.getHttp(url)

        rank = [
            x.find("em").text for x in bs_info.find_all(
                'div', {
                    'class': 'pic'})]
        print(rank)
        title = [
            x.find(
                'span', {
                    'class': 'title'}).text for x in bs_info.find_all(
                'div', {
                    'class': 'hd'})]
        href = [x.find('a').get('href')
                for x in bs_info.find_all('div', {'class': 'hd'})]
        star = [
            x.text for x in bs_info.find_all(
                'span', {
                    'class': 'rating_num'})]
        comment_num = [x.contents[7].text[:-3]
                       for x in bs_info.find_all('div', {'class': 'star'})]
        # 非常喜欢用select，但是find_all速度是2到3倍，放弃
        #comment_num = [x.text[:-3] for x in bs_info.select("body div.star span:last-child")]
        print('列表读取完毕')
        sum = []
        global queue
        global pages
        global isEnd
        for i in range(0, 25):
            comment_top5 = self.getComment(href[i])
            # sleep(1)
            # print(comment_top5)
            queue.put([title[i], star[i], comment_num[i],
                       comment_top5[0],
                       comment_top5[1],
                       comment_top5[2],
                       comment_top5[3],
                       comment_top5[4],
                       rank[i]])
            print(f'{title[i]}评论读取完毕')
            print(queue.qsize())
        return True


if __name__ == '__main__':
    isEnd = False
    pages = Queue(11)
    urls = tuple(
        [f'https://movie.douban.com/top250?start={str(x)}' for x in range(0, 226, 25)])
    for i in urls:
        pages.put(i)
    queue = Queue(100)

    class ProducerThread(Thread):
        def run(self):
            global pages
            global isEnd
            dob = Douban()
            while True:
                url = pages.get()
                dob.maker(url)
                pages.task_done()
                if (pages.empty()):
                    break

    class ConsumerTheard(Thread):
        def run(self):
            global queue
            global isEnd
            with open("douban_movie250_t" + ".csv", "w+", newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['电影名', '评分', '短评数量', '评论1',
                                 '评论2', '评论3', '评论4', '评论5', '排名'])
                while True:
                    item = queue.get()
                    writer.writerow(item)
                    queue.task_done()
                    print(queue.qsize())
                    print(active_count())
                    # if ((isEnd == True) & (queue.empty() == True)):
                    #     break

    p1 = ProducerThread(name='p1')
    p1.start()
    p2 = ProducerThread(name='p2')
    p2.start()
    p3 = ProducerThread(name='p3')
    p3.start()

    c1 = ConsumerTheard(name='c1')
    c1.start()
