from flask import Flask,render_template,redirect,url_for,request

app = Flask(__name__)

@app.route('/')
def index():
    title="¡Bienvenido!"
    return render_template('index.html',titulo=title)

@app.route('/sobre_nosotros')
def sobre_nosotros():
    title="¡Sobre Nosotros!"
    return render_template('sobre_nosotros.html',titulo=title)

@app.route('/biblioteca')
def biblioteca():
    title="Biblioteca"
    return render_template('biblioteca.html',titulo=title)

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
        contrasena = request.form.get('contrasena_registro')
        return redirect(url_for('index',user=usuario,email=mail,password=contrasena))
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

if __name__ == "__main__":
    app.run("localhost", port="5000",debug=True)
