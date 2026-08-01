import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://store.steampowered.com/category/"
f = open("category_urls.txt", "r")
for line in f:
    print(f.readline())

#content = requests.get(url).text
#soup = BeautifulSoup(content, 'html.parser')
#tags = soup.find_all("div", class_ = "tab_item_title")
#for tag in tags:
    #print(tag.text)
