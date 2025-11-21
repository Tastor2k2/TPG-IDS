import os
from dotenv import load_dotenv
import mysql.connector

# Carga el .env desde el root del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(DOTENV_PATH)

# Ruta segura al archivo SQL
SQL_PATH = os.path.join(os.path.dirname(__file__), "init_db.sql")

with open(SQL_PATH) as f:
    sql = f.read()

# Conexión a MySQL sin seleccionar DB todavía
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cursor = conn.cursor()

# Ejecuta cada statement separado por ;
for statement in sql.split(";"):
    if statement.strip():
        print(statement)
        cursor.execute(statement)
        conn.commit()
        print("Statement executed")

cursor.close()
conn.close()
