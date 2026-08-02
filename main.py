import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def find_app_ids(limit = 200):
    #create a dictionary that maps app id to app name
    #each "page" of the search has 50 games
    count_per_page = 50
    dict = {}
    for start in range(0, limit, count_per_page):
        url = "https://store.steampowered.com/search/results/"
        param_grid = {
                'query' : '',
                'start' : start,
                'count' : count_per_page,
                'infinite' : 1,
                'cc': 'us',
                'l': "english"
        }
        print(f"start: {start}")
        content = requests.get(url, params = param_grid)
        json_data = content.json()
        #obtain the HTML chunk
        html_chunk = json_data.get('results_html', '')

        if not html_chunk:
            print("No more games found.")
            break


        soup = BeautifulSoup(html_chunk, 'html.parser')
        search_result = soup.find_all("a", class_ = "search_result_row")
        search_result = search_result[0:100]
        
        for game in search_result:
            game_name = game.find("span", class_ = "title")
            game_id = game["data-ds-appid"]
            dict[game_id] = game_name.text

        time.sleep(0.5)

    return dict

print(len(find_app_ids(249)))

def visit_page(dict):
    base_url = "https://store.steampowered.com/app/"
    #https://store.steampowered.com/app/730/CounterStrike_2/
    #example app format: url + id + "/" + Name + "/"
    for key in dict:
        game_name = dict[key]
        url = base_url + id + "/" + game_name + "/"
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'html.parser')
        search_result = soup.find()