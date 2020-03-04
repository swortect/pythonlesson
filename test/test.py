class ProducerThread(Thread):
    def run(self):
        global queue
        global num
        path='a.txt'
        with open(path, 'w+', encoding='utf-8') as f:
            while True:
                if(num>5):
                    break
                print('in'+str(num))
                f.write('in'+str(num))
                num=num+1
                time.sleep(1)