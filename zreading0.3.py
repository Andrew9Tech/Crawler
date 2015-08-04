# -*- coding: utf-8 -*-
#---------------------------------------
#   程序：左岸读书博客爬虫
#   版本：0.3
#   作者：andrew9tech
#   日期：2014-12-09
#   语言：Python 2.7
#   操作：输入网址后保存整个博客文章
#   功能：将所有人发布的内容打包txt存储到本地。
#
#   还是有些小Bug，对于IOError捕获，存在页面跳转，
#   可以获得跳转页面的内容，也能匹配出文章名字，但是错的
#   希望能够完善下存在页面跳转后的输出，出错后返回错误类型，不输出错误的文章名称
#---------------------------------------
 
import string
import urllib2
import re

#----------- 处理页面上的各种标签 -----------
class HTML_Tool:
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")
    
    # 用非 贪婪模式 匹配 任意<>标签
    EndCharToNoneRex = re.compile("<.*?>")

    # 用非 贪婪模式 匹配 任意<p>标签
    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")

    # 将一些html的符号实体转变为原始符号
    replaceTab = [("&lt;","<"),("&gt;",">"),("&amp;","&"),("&amp;","\""),("&nbsp;"," ")]
    
    def Replace_Char(self,x):
        x = self.BgnCharToNoneRex.sub("",x)
        x = self.BgnPartRex.sub("\n    ",x)
        x = self.CharToNewLineRex.sub("\n",x)
        x = self.CharToNextTabRex.sub("\t",x)
        x = self.EndCharToNoneRex.sub("",x)

        for t in self.replaceTab:  
            x = x.replace(t[0],t[1])  
        return x  
    
class Zreading_Spider:
    # 申明相关的属性
    def __init__(self,url):  
        self.myUrl = url
        self.datas = []
        self.myTool = HTML_Tool()
        print u'已经启动左岸读书博客爬虫，咔嚓咔嚓'
  
    # 初始化加载页面并将其转码储存
    def zreading_main(self):

        myPage = urllib2.urlopen(self.myUrl).read().decode("utf-8")
        # 计算博客共有多少篇文章
        ArticleNum = self.Article_counter(myPage)
        print '\n'

        #更改range选择保存文章的数目  如：rangge(0, ArticleNum)保存所有文章       
        for Article_Num in range(0,ArticleNum):
            # 读取页面的原始信息并将其从utf-8转码
            ArticleUrl = self.myUrl + '/archives/' + str(Article_Num) + '.html'
            try:
                myArticle = urllib2.urlopen(ArticleUrl).read().decode("utf-8")
                
                # 获取文章的标题
                title = self.find_title(myArticle)
                print u'文章名称：' + title

                # 获取最终的数据，并保存
                self.save_data(ArticleUrl,title)

            except Exception as e:
                print type(e)
                print '该地址' + (ArticleUrl) +'不存在'
                print '\n'


                

    #用来计算一共有多少篇文章
    def Article_counter(self,myPage):
        # 匹配 "共有<article class="entry-common clearfix" data-id="(.*?)" 来获取一共有多少篇文章
        myMatch = re.search(r'<article class="entry-common clearfix" data-id="(.*?)"', myPage, re.S)
        if myMatch:  
            ArticleNum = int(myMatch.group(1))
            print u'爬虫报告：发现博客共有%d篇文章' % ArticleNum
        else:
            ArticleNum = 0
            print u'爬虫报告：无法计算博客有多少篇文章！'
        return ArticleNum

    # 用来寻找文章的标题
    def find_title(self,myArticle):
        # 匹配 <h2 class="entry-name" itemprop="headline">xxxxxxxxxx</h2> 找出标题
        myMatch = re.search(r'<h2.*?>(.*?)</h2>', myArticle, re.S)
        title = u'暂无标题'
        if myMatch:
            title  = myMatch.group(1)
        else:
            print u'爬虫报告：无法加载文章标题！'
        title = title.replace(' ','').replace('\n','')
        return title


    # 用来存储博客文章的内容
    def save_data(self,url,title):
        # 加载页面数据到数组中        
        article = urllib2.urlopen(url).read().decode("utf-8")
        self.deal_data(article)        
        # 打开本地文件
        f = open(title+'.txt','w+')
        f.writelines(self.datas)
        f.close()
        print u'爬虫报告：文件已下载到本地并打包成txt文件'
        print '\n'
            

    # 将内容从页面代码中抠出来
    def deal_data(self,article):
        #清洗内容
        #<div class="entry-content" itemprop="description">(.*?)<div class="wumii-hook"> 
        #当然有很多种正则表达式可以完成,下面包含题目及标签
        #<h2 class="entry-name" itemprop="headline">(.*?)<div class="wumii-hook">
        myItems = re.findall('<h2.*?>(.*?)<div class=.*?>',article,re.S)
        for item in myItems:
            data = self.myTool.Replace_Char(item.replace("\n","").encode("utf-8"))
            print data
            self.datas.append(data+'\n')



#-------- 程序入口处 ------------------
print u"""
#---------------------------------------
#   程序：左岸读书博客爬虫
#   版本：0.3
#   作者：andrew9tech
#   日期：2014-12-09
#   语言：Python 2.7
#   操作：输入网址后保存整个博客文章
#   功能：将所有人发布的内容打包txt存储到本地。
#---------------------------------------
"""

# 以左岸读书博客为例子  下面的URL表示博客的第二页
# bdurl = 'http://www.zreading.cn/page/2'

bdurl = 'http://www.zreading.cn'


if __name__== "__main__":	
    mySpider = Zreading_Spider(bdurl)
    mySpider.zreading_main()
