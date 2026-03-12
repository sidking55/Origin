Airflow MarketVol Data Pipeline (AAPL & TSLA)

Project Overview

The workflow:

* Downloads 1-minute interval stock data from Yahoo Finance
* Processes two symbols: **AAPL** and **TSLA**
* Saves data as CSV files
* Moves files to a shared location (simulating HDFS staging)
* Runs a custom query on both datasets
* Executes in parallel using Celery
* Runs automatically at **6:00 PM, Monday–Friday**

Architecture

Services run via Docker Compose:

* Airflow Webserver
* Airflow Scheduler
* Airflow Worker (Celery)
* Redis (Celery broker)
* Postgres (Airflow metadata DB)
* HDFS (Hadoop container)

Prerequisites

You only need:

Docker Desktop installed and running

No local Python or Airflow installation required.

Project Structure


airflow-marketvol/
│
├── docker-compose.yml
├── dags/
│   └── marketvol.py
├── logs/
├── plugins/
└── README.md

Setup Instructions

Step 1 — Clone or Create Project Folder

bash
mkdir airflow-marketvol
cd airflow-marketvol


Step 2 — Create `docker-compose.yml`

Create a file named:


docker-compose.yml
Paste the provided Docker Compose configuration into it.


Step 3 — Create Required Directories

bash
mkdir dags logs plugins

Step 4 — Add DAG File

Create:


dags/marketvol.py
Paste the provided Airflow DAG code into this file.

Start Airflow

Initialize Airflow

bash
docker compose up airflow-init


Wait until it completes successfully.


Start All Services

bash
docker compose up -d

Access Airflow UI

Open your browser:


http://localhost:8080
Login credentials:
Username: airflow
Password: airflow


DAG Configuration

* DAG Name: `marketvol`
* Schedule: `0 18 * * 1-5`
* Runs: 6 PM, Monday–Friday
* Retries: 2
* Retry Delay: 5 minutes
* Executor: CeleryExecutor

Workflow Execution Order

t0  → Create execution-date directory

t1  → Download AAPL
t2  → Download TSLA
       (Runs in parallel)

t3  → Move AAPL file
t4  → Move TSLA file
       (Runs in parallel)

t5  → Run custom query on both datasets

Dependencies:

* t1 & t2 run after t0
* t3 runs after t1
* t4 runs after t2
* t5 runs after both t3 and t4 complete

Testing the DAG

1. Turn ON the DAG in Airflow UI
2. Click **Trigger DAG**
3. Go to **Graph View**
4. Verify:

   * Parallel execution of t1 & t2
   * Parallel execution of t3 & t4
   * t5 runs last
5. Check logs inside each task


Verifying Results

Inside task logs for `t5`, you should see:


AAPL Avg Close: <value>
TSLA Avg Close: <value>


You can also verify inside container:

bash
docker compose exec airflow-webserver bash
ls /tmp/data/

Running for Two Days

Let the scheduler run naturally at 6 PM for two weekdays.

To manually capture logs:

bash
docker compose logs > scheduler_log.txt

Stop Services

bash
docker compose down


To fully reset:

bash
docker compose down -v
