from flask import Flask,render_template
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
from blueprints.busqueda.busqueda import busqueda_bp
from blueprints.mis_libros.mis_libros import mis_libros_bp

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
app.register_blueprint(busqueda_bp, url_prefix="/busqueda")
app.register_blueprint(mis_libros_bp, url_prefix="/mis_libros")

@app.context_processor
def inject_globals():
    return {
        'BACK_URL': app.config['BACK_URL']
    }

# Manejador de errores:
@app.errorhandler(400)
def page_not_found(error):
    # Renderiza la plantilla 400.html, pasando el error a la plantilla
    return render_template('400.html', error=error), 400

@app.errorhandler(401)
def page_not_found(error):
    return render_template('401.html', error=error), 401

@app.errorhandler(403)
def page_not_found(error):
    return render_template('403.html', error=error), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html', error=error), 500

if __name__ == "__main__":
    app.run("localhost", port="5000",debug=True)
