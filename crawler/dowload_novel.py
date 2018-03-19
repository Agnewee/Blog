# coding: utf-8
"""
小说只能在线观看，有点麻烦，下载到本地保存为txt文本
下载www.biquge.cc网站的小说
"""
from __future__ import print_function
import sys

import requests
from bs4 import BeautifulSoup

if sys.version_info.major > 2:
    from urllib.parse import urljoin
else:
    from urlparse import urljoin


header = {
         'Accept': 'text/html',
         'User-Agent': 'Mozilla/5.0'
         }


def get_content(resource_url, http_header):
    res = requests.get(resource_url, headers=http_header)
    res.encoding = 'gbk'
    if res.status_code == 200:
        return res.text
    else:
        return None


def get_sections_url(soup, div_id):
    urls = (url.get('href') for url in soup.find(id=div_id).find_all('a'))
    return urls


base_url = 'http://www.xbiquge.cc'
book_id = input('清输入小说书号: ')
book_base_url = 'book/{}'.format(book_id)
url = urljoin(base_url, book_base_url)
html = get_content(url, header)
if not html:
    print('获取书籍页面失败，请确认')
    print('退出下载')
    sys.exit(1)

soup = BeautifulSoup(html, 'html.parser')
book_name = soup.h1.text
sections_url = get_sections_url(soup, 'list')


# TODO: 目前下载速度稍慢，有待优化
with open('{}.txt'.format(book_name), 'w+') as f:
    for section in sections_url:
        section_url = urljoin(base_url, '{}/{}'.format(book_base_url, section))
        html = get_content(section_url, header)
        soup = BeautifulSoup(html, 'html.parser')
        section_name = soup.h1.text
        content = '{}\n{}\n'.format(soup.h1.text, soup.find(id='content').text)
        f.write(content)
