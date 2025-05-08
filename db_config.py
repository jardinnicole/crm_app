import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),  # Use 127.0.0.1 not localhost
    user=os.getenv('DB_USER'),
    passwd=os.getenv('DB_PASSWORD')
)

# cursor object

cursor_object = db.cursor()

cursor_object.execute("CREATE DATABASE crm_db")

print("Database created.")