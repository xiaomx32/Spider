import re
import time
import requests
import threading
import queue as Queue
from fake_useragent import UserAgent

# 构造链接列表和章节列表
url_list = []
url_0 = 'https://www.37zww.net/2/2509/'
headers_0 = {'User-Agent': UserAgent().random}
html_0 = requests.get(url=url_0, headers=headers_0)
html_0.encoding = 'gbk'
postfixs = re.findall('<dd><a href="(.*?)"', html_0.text)
bookname = re.findall('class="qq">(.*?)</a?', html_0.text)
for postfix in postfixs:
    url = url_0 + postfix
    url_list.append(url)

start = time.time()
class myThread(threading.Thread):

    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q

    def run(self):
        print('Starting ' + self.name)
        while True:
            try:
                crawler(self.name, self.q)
            except:
                break
        print('Exiting ' + self.name)

def crawler(threadName, q):
    global index
    index += 1
    url = q.get(timeout=2)
    headers = {'User-Agent': UserAgent().random}
    try:
        html = requests.get(url=url, headers=headers, timeout=20)
        html.encoding = 'gbk'
        content = re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<', html.text)
        with open('斗罗大陆-绝世唐门4.0.txt', 'a', encoding='utf-8') as f:
            f.write(bookname[index] + '\n')
            for j in content:
                f.write(j + '\n' + '\n')
        print(q.qsize(), threadName, '写入文件: {}'.format(bookname[index]))
    except Exception as e:
        print(q.qsize(), threadName, html.status_code, e)

index = -1
threadList = ['Thread-1', 'Thread-2', 'Thread-3', 'Thread-4', 'Thread-5', 'Thread-6']
workQueue = Queue.Queue(len(url_list))
threads = []

# 创建新线程
for tName in threadList:
    thread = myThread(tName, workQueue)
    thread.start()
    threads.append(thread)

# 填充队列
for url in url_list:
    workQueue.put(url)

# 等待所有线程完成
for t in threads:
    t.join()

end = time.time()
print('Queue 多线程爬虫的总时间为:', end-start)
print('Exiting Main Thread')
# 219秒
# 185秒
# 193秒


