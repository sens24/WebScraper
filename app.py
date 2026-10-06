import pandas as pd
import streamlit as st
import requests
import json

base_url = "http://127.0.0.1:8000/"

st.title("Steam Analytics")
st.header("Game Charts", divider = "rainbow")
st.sidebar.write("Navigation")
sidebar = st.sidebar.selectbox("Select:", ["Charts", "Search"])

if sidebar == "Charts":
    st.subheader("Top Discounts")
    response = requests.get(base_url + "api/games/top_discounts")
    discount_data = response.json()
    df_discounts = pd.DataFrame(discount_data["top_discounts"])
    df_discounts.index = df_discounts.index+1
    df_discounts = df_discounts.rename(
        columns={
            "game_name": "Game Title",
            "developer": "Developer",
            "price": "Price ($)",
            "discount": "Discount ($)",
                "discount_pct": "Discount (%)",
        }
        )
    st.dataframe(df_discounts)

    st.subheader("Top Rated")
    response = requests.get(base_url + "api/games/top_reviews")
    reviews_data = response.json()
    df_reviews = pd.DataFrame(reviews_data["top_reviews"])
    df_reviews.index = df_reviews.index+1
    df_reviews = df_reviews.rename(columns = {
        "game_name": "Game Title",
        "developer": "Developer",
        "total_reviews" : "Total Reviews",
        "positive_reviews_pct": "Positive Review %",
    })
    st.dataframe(df_reviews)


if sidebar == "Search":
    #page 2
    game_name = st.text_input("What game are you looking for?")
    if game_name:
        url = base_url + "api/games/search/" + game_name
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            search_df = pd.DataFrame(data.get("data", []))
            search_df = search_df.rename(
                columns={
                    "developer": "Developer",
                    "price": "Price ($)",
                    "discount_pct": "Discount (%)",
                    "discount": "Discounted Price ($)",
                    "total_reviews": "Total Reviews",
                    "positive_reviews": "Positive Reviews"
                }
            )
            st.dataframe(search_df, hide_index = True)
        else:
            st.error("Invalid Game Name")

    #price history
    game_name = st.text_input("What game do you want to pull up the price history for?")
    if game_name:
        response = requests.get(base_url + f"api/games/price_history/{game_name}")
        if response.status_code == 200:
            price_history = response.json()
            df_ph = pd.DataFrame(price_history.get("data", []))
            df_ph = df_ph.rename(columns = {
                                            "price": "Price",
                                            "discount_pct": "Discount %",
                                            "discount": "Discount",
                
            })
            df_ph.index = df_ph.index+1
            st.dataframe(df_ph)
            df_ph["Discount Amount"] = df_ph["Price"] - df_ph["Discount"]
            st.subheader("Price in $ Over Snapshots")
            st.line_chart(df_ph, y = "Discount Amount")
        else:
            st.error("Invalid Game Name")

