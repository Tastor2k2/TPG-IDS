import os
from dotenv import load_dotenv
import mysql.connector

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DOTENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(DOTENV_PATH)

SQL_PATH = os.path.join(os.path.dirname(__file__), "init_db.sql")

with open(SQL_PATH) as f:
    sql = f.read()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cursor = conn.cursor()

for statement in sql.split(";"):
    if statement.strip():
        print(statement)
        cursor.execute(statement)
        conn.commit()
        print("Statement executed")

cursor.close()
conn.close()
