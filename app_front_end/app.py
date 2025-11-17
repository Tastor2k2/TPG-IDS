from flask import Flask,render_template,redirect,url_for,request,jsonify
from flask_mail import Mail, Message
from back.src.routes.registrarse import insertar_usuario

app = Flask(__name__)

API_URL = 'localhost:6000/'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'amigosporeldeporte123@gmail.com'
app.config['MAIL_PASSWORD'] = 'btdu souy tqbh ljeb'
app.config['MAIL_DEFAULT_SENDER'] = 'amigosporeldeporte123@gmail.com'

mail = Mail(app)

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




#traigo los libros del usuario desde la db
@app.route('/biblioteca')
def biblioteca():
    tematicas = [
        {
            "id": "algebra",
            "titulo": "Álgebra",
            "publicaciones": [
                {"titulo": "Álgebra de Baldor", "autor": "A. Baldor", "imagen": "images/algebra1.png",
                 "usuario": "Ana López", "facultad": "UNSa"},
                {"titulo": "Álgebra de Baldor", "autor": "A. Baldor", "imagen": "images/algebra1.png",
                 "usuario": "Carlos Díaz", "facultad": "UBA"},
                 {"titulo": "Álgebra de Baldor", "autor": "A. Baldor", "imagen": "images/algebra1.png",
                 "usuario": "Ana Lópes", "facultad": "UNSa"},
                 {"titulo": "Álgebra de Baldor", "autor": "A. Baldor", "imagen": "images/algebra1.png",
                 "usuario": "Ana Lópen", "facultad": "UNSa"},
                 {"titulo": "Álgebra de Baldor", "autor": "A. Baldor", "imagen": "images/algebra1.png",
                 "usuario": "Ana Lópe", "facultad": "UNSa"},
                 {"titulo": "Álgebra de Baldor", "autor": "A. Baldor", "imagen": "images/algebra1.png",
                 "usuario": "Ana Ló", "facultad": "UNSa"},
                 {"titulo": "Álgebra de Baldor", "autor": "A. Baldor", "imagen": "images/algebra1.png",
                 "usuario": "Ana L", "facultad": "UNSa"},
                 {"titulo": "Álgebra de Baldor", "autor": "A. Baldor", "imagen": "images/algebra1.png",
                 "usuario": "Ana López", "facultad": "UNSa"},

            ],
        },
        {
            "id": "analisis",
            "titulo": "Análisis Matemático",
            "publicaciones": [
                {"titulo": "Cálculo I", "autor": "James Stewart", "imagen": "images/analisis1.png",
                 "usuario": "Lucía Torres", "facultad": "UTN"}
            ],
        },
        {
            "id": "ids",
            "titulo": "Introducción al desarrollo de software",
            "publicaciones": [
                {"titulo": "HTML & CSS", "autor": "Thomas A. Powell", "imagen": "images/ids6.png",
                 "usuario": "Nacho Gómez", "facultad": "UBA"}
            ],
        },
    ]
    return render_template("biblioteca.html", tematicas=tematicas)



#mail para solicitar el intercambio (sujeto a cambio con la integracion de la db)

@app.route('/solicitud_intercambio', methods=['GET', 'POST'])
def formulario_intercambio():
    #aca buscamos el libro en la db
    if request.method == 'POST':
        nombre_solicitante = request.form.get('nombre-solicitante')
        apellido_solicitante = request.form.get('apellido-solicitante')
        mail_solicitante = request.form.get('mail-solicitante')
        libro_solicitar = request.form.get('libro-solicitar')
        libro_intercambiar = request.form.get('libro-intercambiar')
        propietario = request.form.get('propietario')

        msg = Message(
            subject="Nueva solicitud de intercambio",
            recipients=[mail_solicitante, "provisorio@gmail.com"]  #uso los del propietario y solicitante (db)
        )

        msg.html = render_template("mail_intercambio.html",
                                   nombre_solicitante=nombre_solicitante,
                                   apellido_solicitante=apellido_solicitante,
                                   mail_solicitante=mail_solicitante,
                                   libro_solicitar=libro_solicitar,
                                   libro_intercambiar=libro_intercambiar,
                                   propietario=propietario)
        mail.send(msg)
        return redirect(url_for('biblioteca'))

    else:
        libro_solicitar = request.args.get('libro', '')
        propietario = request.args.get('propietario', '')
        return render_template('formulario_intercambio.html',
                               tematicas=[],
                               libro_seleccionado=libro_solicitar,
                               propietario=propietario)

if __name__ == "__main__":
    app.run("localhost", port="5000",debug=True)