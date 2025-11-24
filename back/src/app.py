from flask import Flask
from routes.carga_libros import carga_libros_bp
from routes.datos_usuarios import datos_usuarios_bp
from routes.intercambio_libros import intercambio_libros_bp
from routes.listar_libros import listar_libros_bp
from routes.carga_libros_imagenes import carga_libros_imagenes_bp

app = Flask(__name__)

app.register_blueprint(carga_libros_bp, url_prefix="/libros")
app.register_blueprint(datos_usuarios_bp, url_prefix="/datos")
app.register_blueprint(intercambio_libros_bp, url_prefix="/libros")
app.register_blueprint(listar_libros_bp, url_prefix="/libros")
app.register_blueprint(carga_libros_imagenes_bp, url_prefix="/libros")

@app.route('/')
def index():
    return {"message": "API funcionando"}, 200

if __name__ == "__main__":
    app.run(port=5002, debug=True)


    
