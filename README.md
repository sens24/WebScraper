# Steam Analytics Platform
author: sens24\
This repository contains the code for the steam store web scraper and the frontend created with streamlit\
Built by me to find the latest deals and top rated games on the steam store, live with snapshots of price history
Tech Stack used: Jupyter Notebook, Python (pandas, requests, os), PostgreSQL, SQL, SQLalchemy, BeautifulSoup, streamlit

# Prerequisites
you need uv installed (pip install uv)


## Installation and Setup
To get started, clone the repository and go to the root directory cd WebScraper\
git clone git@github.com:sens24/WebScraper.git\
run the command: uv sync\
then with .env.example as an example, set up the .env file with your own credentials for postgres\
then simply in the terminal run:\
uv run run_app.py\
or\
uv run run_app_first_time.py \
if it is your first time


