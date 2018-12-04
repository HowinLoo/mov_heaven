import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time

def GetHTML(url, headers, code):
    #proxies = {"http":"http://58.252.6.165:9000"}
    try:
        r = requests.get(url, headers)
        r.encoding = code
	
        return r.text
    except:
        return '获取网页错误'
	
def ParseHTML(url_parse, **kwargs):
    soup = BeautifulSoup(url_parse,'html.parser')
    return soup

def PickInfo(url, movie_name):
    CODE = 'gb2312'#编码方式
    HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}#代理头
    Info = {}
    Info['片名'] = movie_name
    
    try:
        mov_link = GetHTML(url, HEADERS, CODE)
        mov_link = ParseHTML(mov_link)
        PageStr = mov_link.find('div', id = 'Zoom').get_text().replace('\u3000','').replace(' ', '').strip()
        try:
            Info['豆瓣评分'] = re.search(r'豆瓣评分(\d.\d)/10from([0-9\,]+)users',PageStr).group(1)
            Info['豆瓣评论人数'] = re.search(r'豆瓣评分(\d.\d)/10from([0-9\,]+)users',PageStr).group(2)
        except:
            Info['豆瓣评分'] = None
            Info['豆瓣评论人数'] = None
        try:
            Info['IMDb评分'] = re.search(r'IMDb评分(\d.\d)/10from([0-9\,]+)users',PageStr).group(1)
            Info['IMDb评论人数'] = re.search(r'IMDb评分(\d.\d)/10from([0-9\,]+)users',PageStr).group(2)
        except:
            Info['IMDb评分'] = None
            Info['IMDb评论人数'] = None
    #    Info['下载地址'] = 
        Info['类型'] = re.search(r'类别(\D{2}/\D{2})',PageStr).group(1)
    #    Info['文件大小'] = 
    #    Info['上映时间'] = 
    #    Info['语言'] = 
    #    Info['片长'] = 
    #    Info['简介'] = 
    except:
        Info = None
    return Info

def RecommendStar():
    pass

def PackUpToCSV(df, save_path = 'D:/Dairly/Code/Git/mov_heaven/'):
    while None in df:
        df.remove(None)
    df = pd.DataFrame(df)
    df.to_csv(save_path + 'TodayMov.csv', index = None, encoding = 'gbk')
#    if None in df:
#        None_numbers = df.count(None)
#        for i in range(None_numbers):
#            df.remove(None)
#    else:
#        df.to_csv(save_path + 'TodayMov.csv', index = None)

    

def main():
    URL = 'http://www.dytt8.net' # 网址
    CODE = 'gb2312' # 网页编码方式
    HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'} # 代理头
    mov_website = GetHTML(URL, HEADERS, CODE) # 获取网页html源代码
    index_attr = {'width':'85%', 'height':22, 'class':'inddline'} # 主页属性
    soup_indexpage = ParseHTML(mov_website) # 将主页做成汤
    index_page = soup_indexpage.find_all('td', limit = 16, attrs = index_attr)
    index_link = ParseHTML(str(index_page)) # 提取信息后在做成汤
    index_link.td.decompose()
    
    for i in range(15): # 去除特性相同而无用的标签
        index_link.find('a',href='/html/gndy/dyzz/index.html').decompose()

    # 将电影名称与链接储存起来
    Infolist = []
    address = []
    movie_names =[]
    for i in index_link('a'):
        address.append('%s%s'%(URL, i['href']))
        movie_names.append(i.get_text())
    for i in range(15):
        time.sleep(5)
        Infolist.append(PickInfo(address[i], movie_names[i]))
    # return moive_names, address
    
    PackUpToCSV(Infolist)
    
    return Infolist

if __name__ == '__main__':
    main()