#!/usr/bin/env python2

# This script scrapes all club comments.

from bs4 import BeautifulSoup
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Obtain the html for the forum frontpage
url = "http://myanimelist.net/clubs.php?id=40791&action=view&t=comments"
headers = {
    'User-Agent': raw_input("Enter your API key: ")
}
html = requests.get(url, headers=headers).text

# Find the number of pages to go through
soup = BeautifulSoup(html, "lxml")
num_pages = int(soup.find("div", attrs={'class': 'borderClass spaceit'}).text.split('(')[1].split(')')[0])
num_digits = len(str(num_pages))

for i in range(num_pages):
    if i > 0:
        url = 'http://myanimelist.net/clubs.php?id=40791&action=view&t=comments&show=' + str(i*20)
        html = requests.get(url, headers=headers).text
    f = open('club-comments/page_' + str(i+1).zfill(num_digits) + '.html', 'w')
    f.write(html)
    f.close()
    # Progress bar
    print 'Page ' + str(i+1) + '/' + str(num_pages) + ': True'
