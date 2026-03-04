**Project Overview**



This project demonstrates a simple ETL (Extract, Transform, Load) pipeline using Python and MySQL.



The application:



Connects to a MySQL database



Creates a sales table using DDL



Loads ticket sales data from third\_party\_sales\_1.csv



Queries the most popular ticket sales from the past month



Displays results in a user-friendly format



This project showcases how to use the MySQL Python connector to interact with a database programmatically.



**Technologies Used**



Python 3.13+



MySQL Server 8+



mysql-connector-python



CSV file handling (Python built-in library)



**Project Structure**

ticket-sales-pipeline/

│

├── ticket\_sales\_pipeline.py

├── third\_party\_sales\_1.csv

├── execution\_log.txt

└── README.md

⚙️ Prerequisites



Before running this project, ensure you have:



Python installed



MySQL Server installed and running



pip installed



To check versions:



python --version

mysql --version

***Step 1 – Install Required Dependency***



Install MySQL connector for Python:



pip3 install mysql-connector-python



Verify installation:



pip3 show mysql-connector-python

🗄 Step 2 – Setup MySQL Database

1️⃣ Login to MySQL

mysql -u root -p

2️⃣ Create the Database

CREATE DATABASE ticket\_sales\_db;

3️⃣ Use the Database

USE ticket\_sales\_db;

***Step 3 – Sales Table DDL***



The application automatically creates the table, but the DDL is shown below for reference:



CREATE TABLE IF NOT EXISTS sales (

&nbsp;   ticket\_id INT PRIMARY KEY,

&nbsp;   trans\_date INT,

&nbsp;   event\_id INT,

&nbsp;   event\_name VARCHAR(50),

&nbsp;   event\_date DATE,

&nbsp;   event\_type VARCHAR(10),

&nbsp;   event\_city VARCHAR(20),

&nbsp;   customer\_id INT,

&nbsp;   price DECIMAL(10,2),

&nbsp;   num\_tickets INT

);

***Step 4 – Configure Database Credentials***



Open:



ticket\_sales\_pipeline.py



Update the connection section:



connection = mysql.connector.connect(

&nbsp;   user='your\_mysql\_username',

&nbsp;   password='your\_mysql\_password',

&nbsp;   host='localhost',

&nbsp;   port='3306',

&nbsp;   database='ticket\_sales\_db'

)

***Step 5 – Run the Data Pipeline***



Make sure the CSV file third\_party\_sales\_1.csv is in the same directory.



Run:



python ticket\_sales\_pipeline.py

**What the Script Does**



✔ Connects to MySQL

✔ Creates the sales table

✔ Loads all CSV records into the table

✔ Queries top 3 most popular events (based on tickets sold in the past month)

✔ Displays results



**Expected Output**

Database connection successful.

Sales table created or already exists.

CSV data successfully loaded into sales table.



Here are the most popular tickets in the past month:

\- The North American International Auto Show

\- Carlisle Ford Nationals

\- Washington Spirits vs Sky Blue FC



Database connection closed.

**How to Verify It Worked**



After running the script, log into MySQL and verify:



USE ticket\_sales\_db;



SELECT COUNT(\*) FROM sales;



SELECT event\_name, SUM(num\_tickets)

FROM sales

GROUP BY event\_name

ORDER BY SUM(num\_tickets) DESC

LIMIT 5;



You should see:



Data successfully inserted



Aggregated ticket totals per event

