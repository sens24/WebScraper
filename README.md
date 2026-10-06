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

First-time setup for Docker/Airflow
Run in PowerShell:

powershell
mkdir airflow-docker; cd airflow-docker
curl.exe -LO "https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml"
mkdir dags, logs, plugins, config
"AIRFLOW_UID=50000" | Out-File -Encoding ascii .env
docker compose up airflow-init

Then copy extract.py, transform.py, load.py, and etl_pipeline.py into dags/.

Usage
From the airflow-docker folder:

powershell
docker compose up -d       # start Airflow\
docker compose ps          # check services are healthy\
docker compose down        # stop and remove containers

Once running:

Open http://localhost:8080\
Log in with airflow / airflow (default for local use only)\
Find etl_pipeline under Dags\
Flip the toggle to unpause it\
Click the trigger (play) button to run it now\
Open the run, click a task, then Logs to see output

By default the DAG also runs on its schedule (@daily).

The DAG
dags/etl_pipeline.py defines three BashOperator tasks that run the scripts in order:

python\
extract >> transform >> load
