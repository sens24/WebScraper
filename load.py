#connect to a postgres database
#Load into a postgres database
import pandas as pd
from dotenv import load_dotenv
import os
import psycopg2
from sqlalchemy import create_engine

def connect():
    load_dotenv()
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_url = f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/steam"

    #to_sql requires an engine
    engine = create_engine(db_url)
    return engine

def read_df():
    df = pd.read("raw/cleaned_steam_games.parquet")
    return df

def split_df(df): #splits the df into two dataframes that abide by the schema
    df_games = df[["GameID", "Name", "Release Date", "Year Released", "Developer", "Publisher", "Genre(s)", "Genre1", "Genre2", "Genre3"]].copy()
    df_games.columns = ["game_id", "name", "release_date", "year_released", "developer", "publisher", "genres",
    "genre_1", "genre_2", "genre_3"]
    df_games = df_games.drop_duplicates(subset=["game_id"]) #preventative measures

    df_price = df[[
    "GameID", "Price", "Discount", "Discount %", "Total Reviews",
    "Positive Reviews", "Negative Reviews", "Positive Reviews %",
    "Negative Reviews %", "Review Sentiment"]].copy()
    df_price.columns = ["game_id", "price", "discount", "discount_pct", "total_reviews", "positive_reviews", "negative_reviews", "positive_reviews_pct", 
                        "negative_reviews_pct", "review_sentiment"]

    
    return df_games, df_price

def load_database(df_games, df_price):
    engine = connect();
    df_games.to_sql("steam_games", con=engine, if_exists="append", index=False)
    df_price.to_sql("steam_price_history", con=engine, if_exists="append", index=False)


def main():
    df = read_df()
    load_database(split_df(df))
    print("Successfully Loaded!\n")