import requests
import re
from bs4 import BeautifulSoup

def GETHTML(url, headers, code):
    try:
        r = requests.get(url, headers)
        r.encoding = code
	
        return r.text
    except:
        return '获取网页错误'
	
def PARSEHTML(url_parse, **kwargs):
    soup = BeautifulSoup(url_parse,'html.parser')
    return soup
    
def main():
    URL = 'http://www.dytt8.net'
    CODE = 'gb2312'#编码方式
    HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}#代理头
    mov_website = GETHTML(URL, HEADERS, CODE)
    index_attr = {'width':'85%', 'height':22, 'class':'inddline'}
    soup_indexpage = PARSEHTML(mov_website)
    index_page = soup_indexpage.find_all('td', limit = 16, attrs = index_attr)
    a = PARSEHTML(str(index_page))
    a.td.decompose()
    #去除特性相同而无用的标签
    for i in range(15):
        a.find('a',href='/html/gndy/dyzz/index.html').decompose()
    #将电影名称与链接储存起来
    moive_names = []
    address = []
    for i in a('a'):
        address.append('%s%s'%(URL, i['href']))
    for i in a('a'):
        moive_names.append(i.get_text())
    
    return moive_names, address

m1 = GETHTML(address[0])
m1s = PARSERHTML(m1)
m1s.find('div', id = 'Zoom')
