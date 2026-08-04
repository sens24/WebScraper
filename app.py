import pandas as pd
import streamlit as st
import requests
import json

base_url = "http://127.0.0.1:8000/"

st.title("Steam Analytics")
st.header("Game Charts", divider = "rainbow")

#refresh button to call the pipeline in the background
st.write("Click this button to rescrape the data!")
refresh_button = st.button("Refresh Data")

if refresh_button:
    url = base_url + "api/admin/run_etl_pipeline"
    response = requests.post(url)
    print(response.json())


col1, col2 = st.columns(2)
