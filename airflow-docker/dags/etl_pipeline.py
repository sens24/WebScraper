from datetime import datetime
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG("etl_pipeline", schedule="@daily",
         start_date=datetime(2026, 1, 1), catchup=False) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="cd /opt/airflow/dags && python scraper.py",
    )
    transform = BashOperator(
        task_id="transform",
        bash_command="cd /opt/airflow/dags && python transform.py",
    )
    load = BashOperator(
        task_id="load",
        bash_command="cd /opt/airflow/dags && python load.py",
    )

    extract >> transform >> load