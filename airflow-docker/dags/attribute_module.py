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

import re

def reviews(soup, game_attributes):
    total = pos = neg = "0"
    sentiment = None

    counts = soup.find_all("span", class_="user_reviews_count")
    if len(counts) >= 3:
        clean = lambda s: s.text.replace("(", "").replace(")", "").replace(",", "").strip()
        total, pos, neg = clean(counts[0]), clean(counts[1]), clean(counts[2])
    else:
        # fallback: parse the summary tooltip (use the last row = all reviews)
        rows = soup.find_all("div", class_="user_reviews_summary_row")
        for row in reversed(rows):
            m = re.search(r"(\d+)% of the ([\d,]+) user reviews", row.get("data-tooltip-html", ""))
            if m:
                pct, n = int(m.group(1)), int(m.group(2).replace(",", ""))
                p = round(n * pct / 100)
                total, pos, neg = str(n), str(p), str(n - p)
                break

    summaries = soup.find_all("span", class_="game_review_summary")
    if summaries:
        sentiment = summaries[-1].get_text(strip=True)

    game_attributes.extend([total, pos, neg, sentiment])
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