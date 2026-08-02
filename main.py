import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def find_app_ids(limit = 200): #set a default limit of 200
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
            if len(dict) == limit:
                print(f"Scraped through {limit} games on Steam!")
                return dict

        time.sleep(0.5)

    return dict

dict = find_app_ids(10)

def visit_page(dict):
    base_url = "https://store.steampowered.com/app/"
    #https://store.steampowered.com/app/730/CounterStrike_2/
    #example app format: url + id + "/" + Name + "/"
    for key in dict:
        #pointing every key (app id) to a list of attributes
        game_attributes = []
        game_name = dict[key]
        game_attributes.append(game_name)

        url = base_url + key + "/" + game_name + "/"
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'html.parser')
        #release_date
        date = soup.find("div", class_ = "release_date")
        game_attributes.append(date.find("div", class_ = "date").text);

        #price
        price = soup.find("div", class_ = "game_purchase_price price")
        game_attributes.append(price.text.strip())

        #developer and publisher
        dev_row = soup.find_all("div", class_ = "dev_row")
        dev = dev_row[0]
        game_attributes.append(dev.find("a").text)
        pub = dev_row[1]
        game_attributes.append(pub.find("a").text)
        #reviews
        total_reviews = soup.find_all("span", class_ = "user_reviews_count")
        total = total_reviews[0]
        positive_reviews = total_reviews[1]
        negative_reviews = total_reviews[2]
        game_attributes.append(total.text.replace('(', '').replace(")", ""))
        game_attributes.append(positive_reviews.text.replace('(', '').replace(")", ""))
        game_attributes.append(negative_reviews.text.replace('(', '').replace(")", ""))

        review_sentiment = soup.find("span", class_ = "game_review_summary")
        game_attributes.append(review_sentiment.text)



        dict[key] = game_attributes
        print(game_attributes)

visit_page(dict)
print(dict)


#for later usage, the dict is structured 
# app_id: [name, date released, price, developer, publisher, total reviews, positive reviews, negative reviews, overall review sentiment, [genres]]