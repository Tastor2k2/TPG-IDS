from flask import Flask
from flask_session import Session 
from config import Config
from flask_cors import CORS
from routes.carga_libros import carga_libros_bp
from routes.datos_usuarios import datos_usuarios_bp
from routes.intercambio_libros import intercambio_libros_bp
from routes.listar_libros import listar_libros_bp

app = Flask(__name__)
app.config.from_object(Config) #carga la configuracion desde config.py
Session(app) #permite almacenar datos de usuarios commo info de autenticacion 
CORS(app)

app.register_blueprint(carga_libros_bp, url_prefix="/libros")
app.register_blueprint(datos_usuarios_bp, url_prefix="/datos")
app.register_blueprint(intercambio_libros_bp, url_prefix="/libros")
app.register_blueprint(listar_libros_bp, url_prefix="/libros")

@app.route('/')
def index():
    return {"message": "API funcionando"}, 200

if __name__ == "__main__":
    app.run(port=6000, debug=True)
    