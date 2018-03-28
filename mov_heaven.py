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
	
def PARSEHTML(url_parse):
    soup = BeautifulSoup(url_parse,'html.parser')
    
def main():
    URL = 'http://www.dytt8.net/'
    CODE = 'gb2312'#编码方式
    HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}#代理头
    mov_website = GETHTML(URL, HEADERS, CODE)
    index_attr = {width:'85%', height:'22', class_:'inddline', limit:16}
    
    return mov_website