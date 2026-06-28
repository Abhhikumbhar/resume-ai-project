import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="resumeai"
)

print("Database Connected Successfully!")