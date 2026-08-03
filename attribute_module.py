def price(soup, game_attributes):
    purchase_block = soup.find("div", class_ = "game_area_purchase_game")
    if not purchase_block:
        purhcase_block = soup.find("div", class_ = "game_area_purchase")
    if not purchase_block:
        game_attributes.append("No Price")
        game_attributes.append("No Discount")
        return game_attributes

    base_price = purchase_block.find("div", "discount_original_price")
    discount_price = purchase_block.find("div", "discount_final_price")
    if base_price and discount_price:
        game_attributes.append(base_price.text.strip())
        game_attributes.append(discount_price.text.strip())
    else:
        price = purchase_block.find("div", class_ = "game_purchase_price")
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
    if not dev_row:
        game_attributes.append("None")
        game_attributes.append("None")
        return game_attributes

    dev = dev_row[0]
    game_attributes.append(dev.find("a").text)
    pub = dev_row[1]
    game_attributes.append(pub.find("a").text)
    
    return game_attributes

def genre(soup, game_attributes):
    genre_list = []
    div = soup.find("div", class_ = "details_block")
    if not div:
        return game_attributes.append(["None"])
    content = div.find("span")
    if not content:
        return game_attributes.append(["None"])
    genres = content.find_all("a")
    if not genres:
        return game_attributes.append(["None"])
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