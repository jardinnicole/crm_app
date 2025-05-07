import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Kisha1121'
)

# cursor object

cursor_object = db.cursor()

cursor_object.execute("CREATE DATABASE crm_db")

print("Database created.")