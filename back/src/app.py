from flask import Flask
from flask_cors import CORS
from back.src.routes.carga_libros import carga_libros_bp
from src.routes.datos_usuarios import datos_usuarios_bp

app = FLASK(__name__)
CORS(app)

app.register_blueprint(carga_libros_bp, url_prefix="/libros")
app.register_blueprint(datos_usuarios_bp, url_prefix="/datos")

if __name__ == "__main__":
    app.run(port=6000, debug=True)
    