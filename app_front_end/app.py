from flask import Flask,render_template
from flask_mail import Mail
from dotenv import load_dotenv
import os
"""
Se importan los blueprints. Estos los usamos para modularizar el proyecto. De esta manera,
logramos mayor orden en el código y obtenemos la posibilidad de reutilizar estos modulos.
Cada blueprint contiene rutas y funciones que llevan a cabo las distintas funcionalidades de
esta web.
"""
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

load_dotenv()

"""
Se crea una instancia de la app. Es importante ya que ayuda a flask a determinar la raiz del proyecto,
lo cual es crucial para que puedan ser localizado los templates y los archivos de la carpeta 'static'.
Se guarda en una constante la URL del back y se usa app.config para usarla en cualquier
lado del aplicativo.
La secret key se usa para la seguridad de Flask. Más que nada con lo que respecta a las sesiones. El servidor
detecta si alguien modificó la cookie de sesion. Sin la clave secreta, la sesión no funciona.
"""

app = Flask(__name__)

BACK_URL = "http://127.0.0.1:5002"
app.config['BACK_URL'] = BACK_URL
app.secret_key = "super_secret"

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == "True"
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == "True"
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

"""
Se registran los blueprints. Cada blueprint encapsula rutas, templates y lógica de una sección.
El parámetro url_prefix define el segmento base bajo el cual se publican todas las rutas de ese módulo.
"""
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
    """
    Incorpora la constatne globales 'BACK_URL' en el contexto de Jinja para las plantillas.
    Esto evita tener que pasarlas manualmente en cada render_template().
    """
    return {
        'BACK_URL': app.config['BACK_URL']
    }

"""
Manejador de errores:
Según el error, se renderiza alguno de estos templates.
"""
@app.errorhandler(404)
def handle_404(error):
    return render_template('404.html', error=error), 404

@app.errorhandler(500)
def handle_500(error):
    return render_template('500.html', error=error), 500

if __name__ == "__main__":
    app.run("localhost", port="5000",debug=True)
