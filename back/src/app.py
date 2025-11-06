from flask import Flask
from flask_cors import CORS
from src.routes.carga_usuarios import carga_usuarios_bp
from src.routes.datos_usuarios import datos_usuarios_bp

app = FLASK(__name__)
CORS(app)

app.register_blueprint(carga_usuarios_bp, url_prefix="/libros")
app.register_blueprint(datos_usuarios_bp, url_prefix="/datos")