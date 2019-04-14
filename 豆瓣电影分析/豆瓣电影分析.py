from bs4 import BeautifulSoup
import random
from  urllib import request
import time
import re
import csv

#使用代理ip和模拟浏览器进入TOP250主页
def get_html(url):
    # 创建请求头
    head = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    # 代理IP列表
    lists = [
            '113.116.56.177:9000'
             ]
    # 生成代理处理器
    print(random.choice(lists))
    ip = request.ProxyHandler({'https': random.choice(lists)})
    # 创建支持HTTP协议的opener对象
    opener = request.build_opener(ip)
    header1 = []
    # 循环遍历请求头
    for key, value in head.items():
        aa = (key, value)
        header1.append(aa)
    # 把请求头信息添加到opener对象中
    opener.addheaders = header1
    datas = opener.open(url)
    html = datas.read().decode('utf-8')
    return html
# def get_html(urls):
#     r=requests.get(urls)
#     r.encoding='utf-8'
#     return r.text

#获取电影详情页中的字段
def get_details(html):
    in_details=BeautifulSoup(html,'html.parser')
    #导演
    director=in_details.find('span',attrs={'class':'attrs'}).find('a').text
    #演员
    act=in_details.find('span',attrs={'class':'actor'}).find('span',attrs={'class','attrs'}).find_all('a')[:4]
    #由于演员存在于单独的span标签，所以会得到所有的演员，所以主演只获取前4位
    actors=[]
    for i in act:
        i1=i.text
        actors.append(i1)

    #电影类型
    seri=in_details.find('div',attrs={'id':'info'}).find_all('span',attrs={'property':'v:genre'})
    series=[]
    for j in seri:
        j1=j.text
        series.append(j1)

    #片长
    runtime=in_details.find('div',attrs={'id':'info'}).find('span',attrs={'property':'v:runtime'}).text
    #上映日期
    releasedate=in_details.find('div',attrs={'id':'info'}).find('span',attrs={'property':'v:initialReleaseDate'}).text
    #国家/地区
    re_list=re.compile('<span class="pl">制片国家/地区:</span> (.*?)<br/>.*?<span class="pl">语言:</span> .*?<br/>',re.S)
    country=re.findall(re_list,html)
    #语言
    re_list_2=re.compile('<span class="pl">制片国家/地区:</span> .*?<br/>.*?<span class="pl">语言:</span> (.*?)<br/>',re.S)
    language = re.findall(re_list, html)
    return runtime,releasedate,country,language,director,actors,series
#保存获取的所有数据
data_list=[]

#获取每一部电影的详情页链接和主页可以获取的信息
def get_data(html):
    data=BeautifulSoup(html,'html.parser')
    divs=data.find_all('div',attrs={'class':'item'})
    for div in divs:

        #电影标题
        title=div.find('span',attrs={'class':'title'}).text
        #排名
        num=div.find('em').text
        #评分
        score=div.find('div',attrs={'class':'star'}).find('span',attrs={'class':'rating_num'}).text
        #评论人数
        commentors=div.find('div',attrs={'class':'star'}).find_all('span')[-1].text.split('人')[0]
        #短评
        try:
            commente=div.find('p',attrs={'class':'quote'}).find('span',attrs={'class':'inq'}).text
        except:
            commente=''
        #详情链接
        link=div.find('div',attrs={'class':'hd'}).find('a')['href']

        #进入详情页获取主页显示不完整的数据
        time.sleep(3)
        link_data=get_html(link)

        in_details = BeautifulSoup(link_data, 'html.parser')
        # 导演
        director = in_details.find('span', attrs={'class': 'attrs'}).find('a').text
        # 演员
        try:
            act = in_details.find('span', attrs={'class': 'actor'}).find('span', attrs={'class', 'attrs'}).find_all('a')[:4]
            # 由于演员存在于单独的span标签，所以会得到所有的演员，所以主演只获取前4位
            actors = []
            for i in act:
                i1 = i.text
                actors.append(i1)
        except:
            actors=''

        # 电影类型
        seri = in_details.find('div', attrs={'id': 'info'}).find_all('span', attrs={'property': 'v:genre'})
        series = []
        for j in seri:
            j1 = j.text
            series.append(j1)

        # 片长
        runtime = in_details.find('div', attrs={'id': 'info'}).find('span', attrs={'property': 'v:runtime'}).text
        # 上映日期
        releasedate = in_details.find('div', attrs={'id': 'info'}).find('span',attrs={'property': 'v:initialReleaseDate'}).text

        re_list = re.compile('<span class="pl">制片国家/地区:</span> (.*?)<br/>.*?<span class="pl">语言:</span> (.*?)<br/>',re.S)
        re_list1 = re.findall(re_list, link_data)
        re_list2=list(re_list1[0])
        # 国家/地区
        country=re_list2[0]
        # 语言
        language =re_list2[1]
        list_1=[num,title,director,actors,country,language,score,commentors,releasedate,runtime,series,commente]
        data_list.append(list_1)
        print(list_1)

#获取250条数据
for i in range(9,10):
    a=get_html('https://movie.douban.com/top250?start={}&filter='.format(i*25))
    get_data(a)

# 保存到csv
with open('DoubanTop250_4.csv','w') as file:
    data=csv.writer(file)
    data.writerow(['num','title','director','actors','country','language','score','commentors','releasedate','runtime','series','commente'])
    data.writerows(data_list)