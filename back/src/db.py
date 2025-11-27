import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DOTENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(DOTENV_PATH)

def get_connection():
    try: 
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        return connection
    except Error as e:  
        print ("No se puedo conectar a MySql", e)
        return None
