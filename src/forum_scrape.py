#!/usr/bin/env python2

# This script scrapes all threads in the forum board.

from bs4 import BeautifulSoup
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Obtain the html for the forum frontpage
url = "http://myanimelist.net/forum/?clubid=40791"
headers = {
    'User-Agent': raw_input("Enter your API key: ")
}
html = requests.get(url, headers=headers).text

# Find the number of pages to go through
soup = BeautifulSoup(html, "lxml")
num_pages = int(soup.find("div", style='float: right;').text.split('(')[1].split(')')[0])

for i in range(num_pages):
    # Progress bar
    print 'Page ' + str(i+1) + ' of ' + str(num_pages) + ':'
    if i > 0:
        url = 'http://myanimelist.net/forum/?clubid=40791&show=' + str(i*20)
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, "lxml")
    # Obtain ids for all threads on the page
    anchors = soup.findAll('a', href=re.compile('^/forum/\?topicid=[0-9]+$'))
    threads = [int(x.attrs['href'].split('=')[-1]) for x in anchors]
    for j in threads:
        # Scrape the thread
        url = 'http://myanimelist.net/forum/?topicid=' + str(j)
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, "lxml")
        title = soup.find('span', attrs={'class':'forum_locheader'}).text.replace('/', '%2F')
        f = open('threads/' + str(title), 'w')
        f.write(html)
        f.close()
        print str(j) + ': True'
