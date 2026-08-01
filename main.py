import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://store.steampowered.com/category/"

content = requests.get(url).text
soup = BeautifulSoup(content, 'html.parser')
tags = soup.find_all("div", class_ = "tab_item_title")
for tag in tags:
    print(tag.text)
