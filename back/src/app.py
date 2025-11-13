from flask import Flask
from flask_cors import CORS
from src.routes.carga_libros import carga_libros_bp
from src.routes.datos_usuarios import datos_usuarios_bp
from src.routes.datos_usuarios import intercambio_libros_bp
from src.routes.datos_usuarios import listar_libros_bp

app = Flask(__name__)
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
    