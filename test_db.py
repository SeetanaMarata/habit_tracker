# test_db.py
import sys

import psycopg2

print(f"Python encoding: {sys.getdefaultencoding()}")
print(f"Filesystem encoding: {sys.getfilesystemencoding()}")

try:
    conn = psycopg2.connect(
        dbname="habit_tracker_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
    )
    print("SUCCESS! Connected to PostgreSQL")
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e)}")
