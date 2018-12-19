# 爬取个人简书 #

### 本节目标 ### 
   
   本案例抓取简书高质量用户的信息，如昵称、id、文章数、文字数、获得的喜欢等。

### 准备工作 ###

   安装 requests、deque、bs4 库。

### 爬取思路 ###

   首先从初始用户，如 [Andchenn](https://www.jianshu.com/users/e4069496e5e6/following) 关注的用户列表开始,获得 Andcheen 所关注的 A、B、C 等 23 个用户。再依次抓 23 个用户已关注的用户。然后循环前两步。


