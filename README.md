# Steam Analytics Platform
author: sens24\
This repository contains the code for the steam store web scraper and the frontend created with streamlit\
Built by me to find the latest deals and top rated games on the steam store, live with snapshots of price history\
How it works: there exists two parts of the program. The pipeline is isolated in the airflow-docker folder that when activated, runs daily\
based on the user needs. The pipeline will scrape the web page of steam, making sure not to trigger steam's HTTP too many requests, gather\
data of each game, their prices, their discounts, and other important statistics and export a csv with all the information\
This csv is then transformed through a python script to meet our database schema and deal with bad/missing values. The script will return\
a cleaned parquet of data\
Finally the parquet will be read by the load script which will load it into the AWS RDS Postgres instance to be read by the other\
portion of the repository\
Part 2 of the repository takes that database and creates a fastAPI api that is locally hosted and can be called by a Streamlit frontend\
to display information such as top discounts currently, game search ups, and more\
Tech Stack used: Jupyter Notebook, Python (pandas, requests, os), PostgreSQL, SQL, SQLalchemy, BeautifulSoup, streamlit, AWS RDS, Airflow, Docker Compose

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


## For Docker/Airflow startup
Open up Docker Desktop\
cd to the airflow-docker folder and run\
docker compose up -d\
open localhost:8080 and login with airflow user, airflow pass\
turn on pipeline if you want daily scraping\
To halt the pipeline -> docker compose down

## Things to Note
If this is your first time running make sure to run the above commands specific to first timers, so that some historic data\
can be loaded into the database so that the app can query it without having to deal with an empty database\
The data takes a LONG time to scrape due to the steam page's lack of information of each game on the main page\
thus I had to find a workaround and visit every game url specifically from the ids gathered from the main page.\
If you want to scrape more games daily than 200, you will have to go into scraper.py and tweak with the find_app_ids\
function parameters. Be warned, the process takes around 4 seconds per game to scrape.