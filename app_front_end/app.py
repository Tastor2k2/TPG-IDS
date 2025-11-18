from flask import Flask,render_template,redirect,url_for,request,jsonify, session
from back.src.routes.registrarse import insertar_usuario
import requests
app = Flask(__name__)
BACK_URL = "http://127.0.0.1:6000"

API_URL = 'localhost:6000/'
app.secret_key = "super_secret" 

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

@app.route('/contacto',methods=['GET','POST'])
def contacto():
    title="¡Contactate con Nosotros!"
    diccionario_horarios = {
        "Lunes":"08:30 - 22:00",
        "Martes":"08:30 - 22:00",
        "Miercoles":"08:30 - 22:00",
        "Jueves":"08:30 - 22:00",
        "Viernes":"08:30 - 22:00",
        "Sábado":"Cerrado",
        "Domingo":"Cerrado"
    }
    if request.method == 'POST':
        nombre = request.form.get('nombre_usuario')
        apellido = request.form.get('apellido_usuario')
        mail = request.form.get('email_usuario')
        telefono = request.form.get('telefono_usuario')
        mensaje = request.form.get('mensaje_usuario')
        return redirect(url_for('formulario_enviado',
                                name=nombre,
                                surname=apellido,
                                email=mail,
                                tel=telefono,
                                mensj=mensaje))
    return render_template('contacto.html',titulo=title,horarios=diccionario_horarios)

@app.route('/iniciar_sesion',methods=['GET','POST'])
def iniciar_sesion():
    title="Iniciar sesión"
    if request.method == 'POST':
        mail = request.form.get('email_usuario')
        contrasena = request.form.get('contrasena_usuario')
        return redirect(url_for('index',email=mail,password=contrasena))
    return render_template('iniciar_sesion.html',titulo=title)

@app.route('/registrarse',methods=['GET','POST'])
def registrarse():
    title="Registrarse"
    if request.method == 'POST':
        usuario = request.form.get('nombre_usuario')
        mail = request.form.get('email_registro')
        mail_confirmacion = request.form.get('email_confirmacion')
        contrasena = request.form.get('contrasena_registro')
        insertar_usuario(usuario,mail,contrasena)
        return redirect(url_for('index',user=usuario,email=mail,mail_conf=mail_confirmacion,password=contrasena))
    return render_template('registrarse.html',titulo=title)

@app.route('/perfil')
def perfil():
    title="Mi Perfil"
    return render_template('perfil.html',titulo=title)


@app.route('/formulario_enviado')
def formulario_enviado():
    title = "Gracias Por Tu Mensaje"
    nombre = request.args.get('name')
    apellido = request.args.get('surname')
    mail = request.args.get('email')
    telefono = request.args.get('tel')
    mensaje = request.args.get('mensj')
    data = (nombre,apellido,mail,telefono,mensaje)
    return render_template('formulario_enviado.html',titulo=title,informacion_usuario=data)



@app.route('/biblioteca')
def biblioteca():
    try:
        response = requests.get(f"{BACK_URL}/libros")
        tematicas = response.json().get("tematicas", [])
    except Exception:
        tematicas = {}
    return render_template("biblioteca.html", tematicas=tematicas)


@app.route("/mis_libros")
def mis_libros():
    usuario_id = session.get("user_id")
    if not usuario_id:
        return redirect(url_for("iniciar_sesion"))
    response = requests.get(f"{BACK_URL}/mis-libros/{usuario_id}")
    libros = response.json().get("libros", [])
    return render_template("mis_libros.html", libros=libros)




@app.route("/formulario_intercambio/<int:id_libro_solicitado>/<int:id_usuario_solicitado>")
def formulario_intercambio(id_libro_solicitado, id_usuario_solicitado):
    usuario_id = session.get("user_id")
    if not usuario_id:
        return redirect(url_for("iniciar_sesion"))
    response = requests.get(f"{BACK_URL}/mis-libros/{usuario_id}")
    mis_libros = response.json().get("libros", [])
    return render_template(
        "formulario_intercambio.html",
        id_libro_solicitado=id_libro_solicitado,
        id_usuario_solicitado=id_usuario_solicitado,
        mis_libros=mis_libros
    )


@app.route("/enviar_intercambio", methods=["POST"])
def enviar_intercambio():
    usuario_id = session.get("user_id")
    data = {
        "id_libro_solicitado": request.form["id_libro_solicitado"],
        "id_libro_ofrecido": request.form["id_libro_ofrecido"],
        "id_usuario_ofrecido": usuario_id,
        "id_usuario_solicitado": request.form["id_usuario_solicitado"],
    }
    response = requests.post(f"{BACK_URL}/solicitar_intercambio", json=data)
    if response.status_code == 201:
        return render_template("formulario_enviado.html")
    else:
        return f"Error al enviar solicitud: {response.text}", 400
    

@app.route("/cargar_libro")
def cargar_libro():
    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion"))
    return render_template("cargar_libro.html")


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