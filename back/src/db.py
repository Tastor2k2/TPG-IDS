import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Determina la ruta del directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Construye la ruta absoluta al archivo .env dentro de BASE_DIR
DOTENV_PATH = os.path.join(BASE_DIR, ".env")

# Carga las variables de entorno definidas en el .env
load_dotenv(DOTENV_PATH)
print(">>> DB_NAME cargado:", os.getenv("DB_NAME"))
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
