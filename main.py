import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import attribute_module

def find_app_ids(begin = 0, limit = 200): #set a default limit of 200
    #create a dictionary that maps app id to app name
    #each "page" of the search has 50 games
    count_per_page = 50
    dict = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    for start in range(begin, begin + limit, count_per_page): #could implement randomization into this, choose a random start point
        url = "https://store.steampowered.com/search/results/"
        param_grid = {
                'query' : '',
                'start' : start,
                'count' : count_per_page,
                'infinite' : 1,
                'cc': 'us',
                'l': "english"
        }
        content = requests.get(url, headers = headers, params = param_grid)

        #print(f"HTTP Status Code: {content.status_code}")
        #print(f"URL Called: {content.url}")
        #print("Response snippet:\n", content.text[:300]) # First 300 characters
        #print("-" * 50)

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
            if game_name.text in ["Steam Machine", "Steam Deck", "Steam Controller"]: #these will cause issues in other code segments
                dict.pop(game_id)
            if len(dict) == limit:
                print(f"Scraping through {limit} games on Steam!\n")
                return dict

        time.sleep(1.5)

    return dict

def visit_page():
    limit = int(input("How many steam games would you like to scrape from the search engine?: "))
    url_visual = input("Would you like to see the scraped games and urls as they are being scraped?: (Y/N) ")
    dict = find_app_ids(begin = 500, limit = limit)
    base_url = "https://store.steampowered.com/app/"
    #https://store.steampowered.com/app/730/CounterStrike_2/
    #example app format: url + id + "/" + Name + "/"

    for key in dict:
        #pointing every key (app id) to a list of attributes
        game_attributes = []
        game_name = dict[key]
        game_attributes.append(game_name)
        print(game_name)
        
        url = base_url + key + "/" + game_name + "/"
        if url_visual == "Y":
            print(f"url: {url}\n")
        content = requests.get(url).text
        time.sleep(3)
        soup = BeautifulSoup(content, 'html.parser')

        attribute_module.get_info(soup, game_attributes)

        dict[key] = game_attributes
        if url_visual == "Y":
            print(str(game_attributes[0]))
    return dict

def transform_df(dict):
    #transform the dictionary into a pandas dataframe
    df = pd.DataFrame.from_dict(dict, orient = "index", columns = ["Name", "Release Date", 
                                                                   "Price", "Discount", "Developer", 
                                                                   "Publisher", "Total Reviews", "Positive Reviews", 
                                                                   "Negative Reviews", "Review Sentiment", "Genre(s)"])
    return df

def transform_csv(df):
    #transform dataframe into a CSV
    df.to_csv("scraped_steam_games_2.csv", index = False)
    print("CSV Outputted Successfully!")

def main():
    dict = visit_page()
    df = transform_df(dict)
    transform_csv(df)


if __name__ == "__main__":
    main()

#for later usage, the dict is structured 
# app_id: [name, date released, price, discounted_price (if exists), developer, publisher, 
# total reviews, positive reviews, negative reviews, overall review sentiment, [genres]]
