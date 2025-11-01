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
    return render_template('contacto.html',titulo=title)

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
