import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def find_app_ids(limit = 200): #set a default limit of 200
    #create a dictionary that maps app id to app name
    #each "page" of the search has 50 games
    count_per_page = 50
    dict = {}
    for start in range(0, limit, count_per_page): #could implement randomization into this, choose a random start point
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
            if game_name.text in ["Steam Machine", "Steam Deck", "Steam Controller"]: #these will cause issues in other code segments
                dict.pop(game_id)
            if len(dict) == limit:
                print(f"Scraping through {limit} games on Steam!\n")
                return dict

        time.sleep(0.5)

    return dict


def price(soup, game_attributes):
    discount = soup.find("div", class_ = "discount_prices")
    if discount != None:
        base_price = soup.find("div", "discount_original_price")
        discount_price = soup.find("div", "discount_final_price")
        if base_price and discount_price: #there exists bundling that does not include base price
            game_attributes.append(base_price.text.strip())
            game_attributes.append(discount_price.text.strip())
        else:
            price = soup.find("div", class_ = "game_purchase_price price")
            if price:
                game_attributes.append(price.text.strip())
                game_attributes.append("No Discount")
            else:
                game_attributes.append("No Price")
                game_attributes.append("No Discount")
    else:
        price = soup.find("div", class_ = "game_purchase_price price")
        if price:
            game_attributes.append(price.text.strip())
            game_attributes.append("No Discount")
        else:
            game_attributes.append("No Price")
            game_attributes.append("No Discount") 

    return game_attributes

def reviews(soup, game_attributes):
    total_reviews = soup.find_all("span", class_ = "user_reviews_count")
    if not total_reviews:
        game_attributes.append("0")
        game_attributes.append("0")
        game_attributes.append("0")
        return game_attributes
    total = total_reviews[0]
    positive_reviews = total_reviews[1]
    negative_reviews = total_reviews[2]
    game_attributes.append(total.text.replace('(', '').replace(")", ""))
    game_attributes.append(positive_reviews.text.replace('(', '').replace(")", ""))
    game_attributes.append(negative_reviews.text.replace('(', '').replace(")", ""))
    
    review_sentiment = soup.find("span", class_ = "game_review_summary")
    game_attributes.append(review_sentiment.text)

    return game_attributes

def release_date(soup, game_attributes):
    date = soup.find("div", class_ = "release_date")
    if date:
        game_attributes.append(date.find("div", class_ = "date").text);
    else:
        game_attributes.append("N/A")
    return game_attributes

def devpub(soup, game_attributes):
    dev_row = soup.find_all("div", class_ = "dev_row")
    dev = dev_row[0]
    game_attributes.append(dev.find("a").text)
    pub = dev_row[1]
    game_attributes.append(pub.find("a").text)
    return game_attributes

def genre(soup, game_attributes):
    genre_list = []
    genres = soup.find("div", class_ = "details_block").find("span").find_all("a")
    for genre in genres:
        genre_list.append(genre.text.strip())
        if len(genre_list) > 3:
            break
    game_attributes.append(genre_list)
    return game_attributes


def visit_page():
    limit = int(input("How many steam games would you like to scrape from the search engine?: "))
    dict = find_app_ids(limit)
    base_url = "https://store.steampowered.com/app/"
    #https://store.steampowered.com/app/730/CounterStrike_2/
    #example app format: url + id + "/" + Name + "/"
    for key in dict:
        #pointing every key (app id) to a list of attributes
        game_attributes = []
        game_name = dict[key]
        game_attributes.append(game_name)
        
        url = base_url + key + "/" + game_name + "/"
        print(f"url: " + url)
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'html.parser')

        #release_date
        release_date(soup, game_attributes)

        #price/discount
        price(soup, game_attributes)

        #developer and publisher
        devpub(soup, game_attributes)

        #reviews
        reviews(soup, game_attributes)

        #genres
        genre(soup, game_attributes)

        dict[key] = game_attributes
        print(game_attributes)
    return dict

place_holder = visit_page()

#for later usage, the dict is structured 
# app_id: [name, date released, price, discounted_price (if exists), developer, publisher, 
# total reviews, positive reviews, negative reviews, overall review sentiment, [genres]]
# make the code more readable -> add functions for every single attribute, and add a gather_info function