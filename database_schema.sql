-- main table
CREATE TABLE steam_games (
    game_id VARCHAR(255) PRIMARY KEY,
    game_name VARCHAR(255),
    release_date DATE,
    year_released INTEGER, 
    developer VARCHAR(255),
    publisher VARCHAR(255),
    genre_list TEXT,
    genre_1 VARCHAR(255),
    genre_2 VARCHAR(255),
    genre_3 VARCHAR(255),
)

-- price history table
CREATE TABLE steam_price_history (
    snapshot_id BIGSERIAL PRIMARY KEY,
    game_id VARCHAR(50) NOT NULL REFERENCES steam_games(game_id) ON DELETE CASCADE
    price NUMERIC(5, 2),
    discount NUMERIC(5, 2),
    discount_pct NUMERIC(5, 2),
    total_reviews INTEGER,
    positive_reviews INTEGER,
    negative_reviews INTEGER,
    review_sentiment VARCHAR(255),
    positive_reviews_pct NUMERIC(5, 2),
    negative_reviews_pct NUMERIC(5, 2)
)


-- ,Name,Release Date,Price,Discount,Developer,Publisher,Total Reviews,Positive Reviews,Negative Reviews,Review Sentiment,Genre(s),Genre1,Genre2,Genre3,Year Released,Discount %,Positive Reviews %,Negative Reviews %
