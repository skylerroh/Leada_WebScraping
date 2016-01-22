import requests
from bs4 import BeautifulSoup, SoupStrainer

search_link = "http://sfbay.craigslist.org/search/sss?query=motorcycles&sort=rel"
r = requests.get(search_link)
raw_html = r.text

soup = BeautifulSoup(raw_html, 'html.parser')

search_results = soup.find_all('a', {'class': 'i'})

 
example_listing = 'http://sfbay.craigslist.org/sby/sys/5371648877.html'
r = requests.get(example_listing)
ad_page_html = r.text
soup = BeautifulSoup(ad_page_html, 'html.parser')
title = soup.find_all('h2', {'class': 'postingtitle'})

for key in title[0]:
   print key