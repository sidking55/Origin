import mysql.connector
import csv
from datetime import datetime, timedelta


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            user='your_username',
            password='your_password',
            host='localhost',
            port='3306',
            database='your_database'
        )
        print("Database connection successful.")
    except Exception as error:
        print("Error while connecting to database:", error)
    return connection


# --------------------------------------------------
# CREATE TABLE
# --------------------------------------------------

def create_sales_table(connection):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS sales (
        ticket_id INT PRIMARY KEY,
        trans_date INT,
        event_id INT,
        event_name VARCHAR(50),
        event_date DATE,
        event_type VARCHAR(10),
        event_city VARCHAR(20),
        customer_id INT,
        price DECIMAL(10,2),
        num_tickets INT
    );
    """
    cursor = connection.cursor()
    cursor.execute(create_table_sql)
    connection.commit()
    cursor.close()
    print("Sales table created or already exists.")


# --------------------------------------------------
# LOAD CSV INTO TABLE
# --------------------------------------------------

def load_third_party(connection, file_path_csv):
    cursor = connection.cursor()

    insert_sql = """
    INSERT INTO sales (
        ticket_id,
        trans_date,
        event_id,
        event_name,
        event_date,
        event_type,
        event_city,
        customer_id,
        price,
        num_tickets
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    with open(file_path_csv, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header

        for row in csv_reader:
            cursor.execute(insert_sql, row)

    connection.commit()
    cursor.close()
    print("CSV data successfully loaded into sales table.")


# --------------------------------------------------
# QUERY MOST POPULAR TICKETS (PAST MONTH)
# --------------------------------------------------

def query_popular_tickets(connection):
    sql_statement = """
    SELECT event_name
    FROM sales
    WHERE event_date >= CURDATE() - INTERVAL 1 MONTH
    GROUP BY event_name
    ORDER BY SUM(num_tickets) DESC
    LIMIT 3;
    """

    cursor = connection.cursor()
    cursor.execute(sql_statement)
    records = cursor.fetchall()
    cursor.close()
    return records


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

def display_results(records):
    print("\nHere are the most popular tickets in the past month:")
    for record in records:
        print(f"- {record[0]}")


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

if __name__ == "__main__":
    connection = get_db_connection()

    if connection:
        create_sales_table(connection)
        load_third_party(connection, "third_party_sales_1.csv")

        records = query_popular_tickets(connection)
        display_results(records)

        connection.close()
        print("\nDatabase connection closed.")