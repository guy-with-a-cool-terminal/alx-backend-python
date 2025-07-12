import mysql.connector
from mysql.connector import Error
import csv
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# function to reuse the database connection yk keep it DRY
def get_connection(use_database=True):
    try:
        conn_args={
            "host": DB_HOST,
            "user": DB_USER,
            "password": DB_PASSWORD
        }
        if use_database:
            conn_args["database"] = DB_NAME
        return mysql.connector.connect(**conn_args)
    except Error as e:
        print(f"Connection failed: {e}")
        return None

# create database if not exists
def create_database():
    conn = get_connection(use_database=False)
    if conn:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        conn.close()

# create table
def create_table():
    conn = get_connection()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    user_id CHAR(36) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    age DECIMAL NOT NULL,
                    INDEX(user_id)
                );
            """)
            conn.commit()
        conn.close()
        print("Table user_data created successfully")

# seeding
def insert_data(csv_file):
    conn = get_connection()
    if conn:
        with conn.cursor() as cursor,open(csv_file,newline='')as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = row.get('user_id') or str(uuid.uuid4())
                cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s;", (user_id,))
                if not cursor.fetchone():
                    cursor.execute("""
                         INSERT INTO user_data(user_id,name,email,age)
                         VALUES (%s,%s,%s,%s);              
                    """, (user_id,row['name'],row['email'],row['age']))
            conn.commit()
        conn.close()

# connect to database(returns a connection without a database selection..)
def connect_db():
    return get_connection(use_database=False)

# connect to database
def connect_to_prodev():
    return get_connection(use_database=True)