from flask import Flask
from blueprints.formulario_enviado.formulario_enviado import formulario_enviado_bp
from blueprints.contacto.contacto import contacto_bp
from blueprints.iniciar_sesion.iniciar_sesion import iniciar_sesion_bp
from blueprints.perfil.perfil import perfil_bp
from blueprints.registrarse.registrarse import registrarse_bp
from blueprints.cerrar_sesion.cerrar_sesion import logout_bp
from blueprints.cargar_libro.cargar_libro import cargar_libro_bp
from blueprints.biblioteca.biblioteca import biblioteca_bp
from blueprints.intercambio.intercambio import intercambio_bp
from blueprints.index.index import index_bp
from blueprints.sobre_nosotros.sobre_nosotros import sobre_nosotros_bp
from blueprints.funcionamiento.funcionamiento import funcionamiento_bp

app = Flask(__name__)
BACK_URL = "http://127.0.0.1:5002"
app.config['BACK_URL'] = BACK_URL
app.secret_key = "super_secret" 

app.register_blueprint(formulario_enviado_bp, url_prefix="/formulario_enviado")
app.register_blueprint(contacto_bp, url_prefix="/contacto")
app.register_blueprint(iniciar_sesion_bp, url_prefix="/iniciar_sesion")
app.register_blueprint(perfil_bp)
app.register_blueprint(registrarse_bp, url_prefix="/registrarse")
app.register_blueprint(logout_bp)
app.register_blueprint(cargar_libro_bp, url_prefix="/cargar_libro")
app.register_blueprint(biblioteca_bp, url_prefix="/biblioteca")
app.register_blueprint(intercambio_bp, url_prefix="/intercambio")
app.register_blueprint(index_bp, url_prefix="/")
app.register_blueprint(sobre_nosotros_bp, url_prefix="/sobre_nosotros")
app.register_blueprint(funcionamiento_bp, url_prefix="/funcionamiento")

@app.context_processor
def inject_globals():
    return {
        'BACK_URL': app.config['BACK_URL']
    }

if __name__ == "__main__":
    app.run("localhost", port="5000",debug=True)
