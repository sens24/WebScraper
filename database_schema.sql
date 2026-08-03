-- main table
CREATE TABLE steam_games (
    game_name VARCHAR(255),
    release_date date,
    developer VARCHAR(255),
    publisher VARCHAR(255),
    genre_list VARCHAR(255),
    genre_1 VARCHAR(255),
    genre_2 VARCHAR(255),
    genre_3 VARCHAR(255),
)

-- price history table
CREATE TABLE steam_price_history (
    price int,
    discount int,
    discount_pct int
)

-- reviews table

CREATE TABLE reviews (
    total_reviews int,
    positive_reviews int,
    negative_reviews int,
    review_sentiment VARCHAR(255),
    positive_reviews_pct int,
    negative_reviews_pct int
)


-- ,Name,Release Date,Price,Discount,Developer,Publisher,Total Reviews,Positive Reviews,Negative Reviews,Review Sentiment,Genre(s),Genre1,Genre2,Genre3,Year Released,Discount %,Positive Reviews %,Negative Reviews %
