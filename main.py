import requests
from bs4 import BeautifulSoup
import pandas as pd


def find_app_ids(limit = 10):
    #create a dictionary that maps app id to app name
    url = "https://store.steampowered.com/search/"
    dict = {}
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'html.parser')
    search_result = soup.find_all("a", class_ = "search_result_row")
    search_result = search_result[0:limit]
    
    for game in search_result:
        game_name = game.find("span", class_ = "title")
        game_id = game["data-ds-appid"]
        dict[game_id] = game_name.text

    print(dict)
find_app_ids(20)
