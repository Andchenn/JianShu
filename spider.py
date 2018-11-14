import re
import csv  # ceil(2.5)返回3
import math
import time
import requests
from collections import deque
from bs4 import BeautifulSoup

# 创建一个csv文件用来收集简书用户信息
path = '../jianshu.csv'
csvFile = open(path, 'a+', newline='', encoding='utf-8')
writer = csv.writer(csvFile)
# csv.writer().writerow()保存的csv文件，打开时每行后都多一行空行
writer.writerow(('id', 'name', 'following', 'follower', 'article', 'word', 'like'))

# 全局变量dict用来储存userid和following关注的人数，后面用来做判断
ID_container = set()

# 用来收集待爬取用户的网址，这里我们的网址是（id，following）
# 需要在后面的函数中构建url
Deque = deque()


class JianShu(object):
    def __init__(self):
        # 定制我们的url模板
        self.user_url = 'http://www.jianshu.com/users/{userid}/following?page={page}'
        # 用户ID与name的匹配规律
        self.IdName_pattern = re.compile('<a class="name" href="/u/(.*?)">(.*?)</a>')
        # 用户的关注，粉丝，文章，文集的匹配规律
        self.meta1_pattern = re.compile(
            '<span>关注 (\d+)</span><span>粉丝 (\d+)</span><span>文章 (\d+)</span>')
        # 用户写的字数，获得的喜欢的匹配模式
        self.meta2_pattern = re.compile('写了 (\d+) 字，获得了 (\d+) 个喜欢')
        # headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 '
                          'Safari/537.36'}

    # 发起请求
    def creat_request(self, userid, page):
        url = self.user_url.format(userid=userid, page=page)
        r = requests.get(url, headers=self.headers).text
        return r

    # 解析用户列表
    def parse_response(self, r):
        soup = BeautifulSoup(r, 'lxml')
        user_List_Container = soup.findAll('ul', {'class': 'user-list'})[0]
        user_List = user_List_Container.contents
        user_List = [str(user) for user in user_List if user != '\n']
        return user_List

    # 解析单个用户信息
    def parser_user_info(self, user):
        Id, Name = re.findall(self.IdName_pattern, user)[0]
        try:
            followingNum, followerNum, articleNum = re.findall(self.meta1_pattern, user)[0]
        except:
            followingNum, followerNum, articleNum = ('', '', '')
        try:
            wordNum, likeNum = re.findall(self.meta2_pattern, user)[0]
        except:
            wordNum, likeNum = ('', '')

        Content = (Id, Name, followingNum, followerNum, articleNum, wordNum, likeNum)
        writer.writerow(Content)
        print(Content)
        return Content

    # 递归方法
    def get_userlist(self, userid, following):
        # 访问的用户的id和following放入ID_container（是一个集合）容器中，以便后面再遇到这个id时，可以验证是否重复访问该id
        ID_container.add((userid, following))
        if following != '':
            num = int(following) / 10
            # ceil(1.8)返回2，ceil(27.8)返回28
            Page = math.ceil(num)
            for page in range(1, Page + 1, 1):
                resp = self.creat_request(userid, page)
                user_List = self.parse_response(resp)
                for user in user_List:
                    content = self.parser_user_info(user)
                    # 将解析出的用户id和following添加到deque队列中去，待爬去
                    Deque.append((content[0], content[2]))
                time.sleep(1)
        # 对队列进行for循环，如果该队列中的元素不在ID_container中，执行函数自身。
        for deq in Deque:
            if deq not in ID_container:
                self.get_userlist(deq[0], deq[1])
                print('hello world')


if __name__ == '__main__':
    JianShu().get_userlist('e4069496e5e6', 23)
