 Airflow Log Analyzer

 Project Overview

This project analyzes Apache Airflow log files and reports all ERROR messages found in the logs.

The application scans all `.log` files recursively in the Airflow log directory and extracts error entries.


 Technologies Used

- Python 3
- pathlib module
- Shell scripting
- Apache Airflow logs



 Airflow Log Location

Airflow logs are configured in:

~/airflow/airflow.cfg

Example configuration:

base_log_folder = ~/airflow/logs

Each DAG has its own log directory.

Example:

~/airflow/logs/marketvol



 Project Files

| File | Description |
|-----|-------------|
| log_analyzer.py | Python script to analyze Airflow logs |
| run_log_analyzer.sh | Shell script to run the analyzer |
| execution_log.txt | Example successful run output |



 How the Program Works

1. The program reads the root Airflow log directory.
2. It recursively scans all `.log` files.
3. Each file is parsed using the `analyze_file()` function.
4. Any log line containing `ERROR` is collected.
5. The total error count and messages are printed.



 How to Run the Program

 Step 1: Clone the repository

```bash
git clone https://github.com/sidking55/Origin
cd airflow-log-analyzer