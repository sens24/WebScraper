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

def get_info(soup, game_attributes):
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