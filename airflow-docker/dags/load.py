#connect to a postgres database
#Load into a postgres database
import pandas as pd
from dotenv import load_dotenv
import os
import psycopg2
from sqlalchemy import create_engine, text

def connect():
    load_dotenv()
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_url = f"postgresql+psycopg2://postgres:{db_password}@host.docker.internal:5432/steam"

    #to_sql requires an engine
    engine = create_engine(db_url)
    return engine

def read_df():
    df = pd.read_parquet("raw/cleaned_steam_games.parquet")
    return df

def split_df(df): #splits the df into two dataframes that abide by the schema
    df_games = df[["GameID", "Name", "Release Date", "Year Released", "Developer", "Publisher", "Genre1", "Genre2", "Genre3"]].copy()
    df_games.columns = ["game_id", "name", "release_date", "year_released", "developer", "publisher",
    "genre_1", "genre_2", "genre_3"]
    df_games = df_games.drop_duplicates(subset=["game_id"]) #preventative measures
    df_games = df_games.drop(columns = ["genres"], errors = "ignore")

    df_price = df[[
    "GameID", "Price", "Discount", "Discount %", "Total Reviews",
    "Positive Reviews", "Negative Reviews", "Positive Reviews %",
    "Negative Reviews %", "Review Sentiment"]].copy()
    df_price.columns = ["game_id", "price", "discount", "discount_pct", "total_reviews", "positive_reviews", "negative_reviews", "positive_reviews_pct", 
                        "negative_reviews_pct", "review_sentiment"]
    #turn game_id into an int
    df_price["game_id"] = pd.to_numeric(df_price["game_id"], errors="coerce")
    df_price = df_price.dropna(subset=["game_id"])
    df_price["game_id"] = df_price["game_id"].astype(int)
    
    return df_games, df_price

def load_database(df_games, df_price):
    engine = connect();

    with engine.begin() as conn:
        df_games.to_sql(
        name="temp_games_staging",
        con=conn,
        if_exists="replace", 
        index=False
    )
        upsert_query = text("""
        INSERT INTO steam_games (game_id, game_name, developer, publisher, genre_1, genre_2, genre_3, release_date, year_released)
        SELECT game_id, name, developer, publisher, genre_1, genre_2, genre_3, release_date, year_released
        FROM temp_games_staging
        ON CONFLICT (game_id) DO UPDATE SET
            game_name = EXCLUDED.game_name,
            developer = EXCLUDED.developer,
            publisher = EXCLUDED.publisher,
            genre_1 = EXCLUDED.genre_1,
            genre_2 = EXCLUDED.genre_2,
            genre_3 = EXCLUDED.genre_3,
            release_date = EXCLUDED.release_date,
            year_released = EXCLUDED.year_released;
    """)
        conn.execute(upsert_query)
        df_price.to_sql("steam_price_history", con=conn, if_exists="append", index=False)


    print("Database updated successfully\n")


def main():
    df = read_df()
    df_games, df_price = split_df(df)
    load_database(df_games, df_price)
    print("Successfully Loaded!\n")

if __name__ == "__main__":
    main()