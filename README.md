# Steam Analytics Platform
author: sens24\
This repository contains the code for the steam store web scraper and the frontend created with streamlit\
Built by me to find the latest deals and top rated games on the steam store, live with snapshots of price history
Tech Stack used: Jupyter Notebook, Python (pandas, requests, os), PostgreSQL, SQL, SQLalchemy, BeautifulSoup, streamlit, Docker, Airflow

The repo consists of two parts, the ETL pipeline to extract transform and load the steam data into your PostgreSQL database with your credentials.\
You must first copy and paste the database_schema.sql file into a database named "steam" or else this program will NOT work.\
The pipeline is bundled in a Docker Compose setup that contains an Airflow DAG to implement the pipeline on a daily running basis (the pipeline is very slow, it will take at minimum 5 hours due to Steam HTTP request limiting)\
Follow the instructions below to access the pipeline.
The second part is the frontend that is in progress where you can see charts and search up games based on your own interests. Follow the Installation and Setup setup below

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

First-time setup for Docker/Airflow
Run in PowerShell:

## For Docker/Airflow startup
Open up Docker Desktop\
cd to the airflow-docker folder and run\
docker compose up -d\
open localhost:8080 and login with airflow user, airflow pass\
turn on pipeline if you want daily scraping
