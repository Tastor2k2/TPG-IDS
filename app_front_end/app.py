from flask import Flask,render_template,redirect,url_for,request,jsonify, session
from blueprints.formulario_enviado.formulario_enviado import formulario_enviado_bp
from blueprints.contacto.contacto import contacto_bp
from blueprints.iniciar_sesion.iniciar_sesion import iniciar_sesion_bp
from blueprints.perfil.perfil import perfil_bp
from blueprints.registrarse.registrarse import registrarse_bp
from blueprints.cerrar_sesion.cerrar_sesion import logout_bp
from blueprints.cargar_libro.cargar_libro import cargar_libro_bp
from blueprints.biblioteca.biblioteca import biblioteca_bp
from blueprints.intercambio.intercambio import intercambio_bp

import requests
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

@app.context_processor
def inject_globals():
    return {
        'BACK_URL': app.config['BACK_URL']
    }

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sobre_nosotros')
def sobre_nosotros():
    title="¡Sobre Nosotros!"
    return render_template('sobre_nosotros.html',titulo=title)

@app.route('/funcionamiento')
def funcionamiento():
    title="¿Cómo Funcionamos?"
    return render_template('funcionamiento.html',titulo=title)

@app.route("/mis_libros")
def mis_libros():
    usuario_id = session.get("user_id")
    if not usuario_id:
        return redirect(url_for("iniciar_sesion"))
    response = requests.get(f"{BACK_URL}/mis-libros/{usuario_id}")
    libros = response.json().get("libros", [])
    return render_template("mis_libros.html", libros=libros)

@app.route("/enviar_carga_libro", methods=["POST"])
def enviar_carga_libro():
    usuario_id = session.get("user_id")
    if not usuario_id:
        return redirect(url_for("iniciar_sesion"))
    data = {
        "titulo": request.form["titulo"],
        "autor": request.form["autor"],
        "codigo_isbn": request.form["codigo_isbn"],
        "editorial": request.form["editorial"],
        "tematica": request.form["tematica"],
        "usuario_id": usuario_id,
        "es_favorito": False
    }
    response = requests.post(f"{BACK_URL}/cargar", json=data)
    if response.status_code == 201:
        return redirect(url_for("mis_libros"))
    return f"Error al cargar libro: {response.text}", 400


@app.route("/favorito/<int:libro_id>", methods=["POST"])
def añadir_favorito(libro_id):
    usuario_id = session.get("user_id")
    if not usuario_id:
        return redirect(url_for("iniciar_sesion"))
    libro = requests.get(f"{BACK_URL}/mis-libros/{usuario_id}").json()
    libro_actual = None
    for l in libro["libros"]:
        if l["id"] == libro_id:
            libro_actual = l
        break
    if not libro_actual:
        return "Libro no encontrado", 404
    nuevo_estado = not libro_actual["es_favorito"]
    data = {
        "usuario_id": usuario_id,
        "es_favorito": nuevo_estado
    }
    requests.put(f"{BACK_URL}/marcar-favorito/{libro_id}", json=data)
    return redirect(url_for("mis_libros"))


@app.route("/eliminar_libro/<int:libro_id>", methods=["POST"])
def eliminar_libro(libro_id):
    usuario_id = session.get("user_id")
    if not usuario_id:
        return redirect(url_for("iniciar_sesion"))
    data = {"usuario_id": usuario_id}
    requests.delete(f"{BACK_URL}/eliminar/{libro_id}", json=data)
    return redirect(url_for("mis_libros"))

if __name__ == "__main__":
    app.run("localhost", port="5000",debug=True)