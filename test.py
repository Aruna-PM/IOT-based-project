import mysql.connector
from mysql.connector import Error
import datetime
import random  # Import the random module

# MySQL configuration
host = 'localhost'  # Change to your MySQL host
user = 'root'       # Change to your MySQL username
password = 'root'  # Change to your MySQL password
database_name = 'reward_system'
table_name = 'rewards'

# Function to create a connection to MySQL server
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        if connection.is_connected():
            print("Connected to MySQL server successfully!")
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Function to create a new database if it doesn't exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' created or already exists.")
    except Error as e:
        print(f"Error while creating database: {e}")

# Function to create a table if it doesn't exist
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"USE {database_name}")
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            serial_id INT AUTO_INCREMENT PRIMARY KEY,
            mobile_no VARCHAR(15) NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            reward_amount DECIMAL(10, 2) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created or already exists.")
    except Error as e:
        print(f"Error while creating table: {e}")

# Function to insert user data into the table
def insert_user_data(connection, mobile_no):
    try:
        cursor = connection.cursor()
        cursor.execute(f"USE {database_name}")
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        # Generate a random reward amount between 50 and 500
        reward_amount = round(random.uniform(1.00, 10.00), 2)

        insert_query = f"""
        INSERT INTO {table_name} (mobile_no, date, time, reward_amount)
        VALUES (%s, %s, %s, %s)
        """
        values = (mobile_no, current_date, current_time, reward_amount)
        cursor.execute(insert_query, values)
        connection.commit()
        print("User data inserted successfully!")
    except Error as e:
        print(f"Error while inserting data: {e}")

# Main function
def database_main(mobile_no):
    connection = create_connection()
    if connection:
        create_database(connection)
        create_table(connection)
        
        insert_user_data(connection, mobile_no)
            
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed.")


database_main("9206639940")
