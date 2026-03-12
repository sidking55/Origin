from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from datetime import date
import yfinance as yf
import pandas as pd
import os

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'marketvol',
    default_args=default_args,
    description='Market volatility pipeline',
    start_date=datetime(2026, 3, 4, 18, 0),
    schedule_interval='0 18 * * 1-5',
    catchup=False
)

# t0 - Create directory
t0 = BashOperator(
    task_id='t0',
    bash_command='mkdir -p /tmp/data/{{ ds }}',
    dag=dag
)

def download_stock(symbol, **context):
    execution_date = context['ds']
    path = f"/tmp/data/{execution_date}/{symbol}.csv"

    start_date = date.today()
    end_date = start_date + timedelta(days=1)

    df = yf.download(symbol, start=start_date, end=end_date, interval='1m')
    df.to_csv(path)

t1 = PythonOperator(
    task_id='t1',
    python_callable=download_stock,
    op_kwargs={'symbol': 'AAPL'},
    dag=dag
)

t2 = PythonOperator(
    task_id='t2',
    python_callable=download_stock,
    op_kwargs={'symbol': 'TSLA'},
    dag=dag
)

# t3 & t4 move to shared location
t3 = BashOperator(
    task_id='t3',
    bash_command='cp /tmp/data/{{ ds }}/AAPL.csv /tmp/data/combined/',
    dag=dag
)

t4 = BashOperator(
    task_id='t4',
    bash_command='cp /tmp/data/{{ ds }}/TSLA.csv /tmp/data/combined/',
    dag=dag
)

def run_query(**context):
    path = "/tmp/data/combined/"
    aapl = pd.read_csv(path + "AAPL.csv")
    tsla = pd.read_csv(path + "TSLA.csv")

    avg_aapl = aapl['Close'].mean()
    avg_tsla = tsla['Close'].mean()

    print("AAPL Avg Close:", avg_aapl)
    print("TSLA Avg Close:", avg_tsla)

t5 = PythonOperator(
    task_id='t5',
    python_callable=run_query,
    dag=dag
)

# Dependencies
t0 >> [t1, t2]
t1 >> t3
t2 >> t4
[t3, t4] >> t5