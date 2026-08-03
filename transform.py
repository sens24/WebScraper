#this file cleans the data and returns a python dataframe to load into the postgres database
#code taken from the testing jupyter notebook
import numpy as np
import pandas as pd

def concat():
    df_1 = pd.read_csv("raw/scraped_steam_games.csv")
    df_2 = pd.read_csv("raw/scraped_steam_games_2.csv")
    df = pd.concat([df_1, df_2]).reset_index(drop = True)
    return df

def release_date(df):
    df["Release Date"] = pd.to_datetime(df["Release Date"], format = "mixed")
    return df

def price(df):
    df["Price"] = df["Price"].replace("Free To Play", "0")
    df["Price"] = df["Price"].replace(to_replace = r"(?i).*Free.*", value = "0", regex = True)
    df["Price"] = df["Price"].replace("No Price", "0")
    df["Price"] = df["Price"].str.replace("/ month", "", regex=False)
    df["Price"] = df["Price"].replace(to_replace = r"(?i).*demo.*", value = "0", regex = True)
    df["Price"] = df["Price"].str.strip("$")
    df["Price"] = df["Price"].astype("float")
    df["Discount"] = df["Discount"].replace("No Discount", "0")
    df["Discount"] = df["Discount"].str.strip("$")
    df["Discount"] = df["Discount"].astype("float")

    return df

def reviews(df):
    df["Total Reviews"] = df["Total Reviews"].str.replace(",", "")
    df["Total Reviews"] = df["Total Reviews"].astype("int64")

    df["Positive Reviews"] = df["Positive Reviews"].str.replace(",", "")
    df["Positive Reviews"] = df["Positive Reviews"].astype("int64")

    df["Negative Reviews"] = df["Negative Reviews"].str.replace(",", "")
    df["Negative Reviews"] = df["Negative Reviews"].astype("int64")
    return df


def genres(df):
    import ast
    df["Genre(s)"] = df["Genre(s)"].fillna("['None', 'None', 'None', 'None']")
    df["Genre(s)"] = df["Genre(s)"].apply(ast.literal_eval)
    df["Genre1"] = df["Genre(s)"].str[0]
    df["Genre2"] = df["Genre(s)"].str[1]
    df["Genre3"] = df["Genre(s)"].str[2]
    return df


def new_feature(df):
    df["Year Released"] = df["Release Date"].dt.year

    df["Discount %"] = round((df["Price"]-df["Discount"])/df["Price"] * 100)
    df["Discount %"] = df["Discount %"].replace(100.0, None)

    df["Positive Reviews %"] = df["Positive Reviews"]/df["Total Reviews"] * 100
    df["Negative Reviews %"] = df["Negative Reviews"]/df["Total Reviews"] * 100

    return df

def transform(df):
    release_date(df)
    price(df)
    reviews(df)
    genres(df)
    new_feature(df)
    return df

def main():
    df = concat()
    transform(df)
    df.to_csv("cleaned_steam_games.csv")

if __name__ == "__main__":
    main()