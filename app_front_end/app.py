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
    materias = [
        {
            "id": "algebra",
            "titulo": "Algebra",
            "libros": [
                {"titulo": "Algebra de Baldor", "autor": "A. Baldor", "imagen": "images/algebra1.png"},
                {"titulo": "Algebra", "autor": "Hames Stewart", "imagen": "images/algebra2.png"},
                {"titulo": "Algebraic Art", "autor": "Andrea K. Henderson", "imagen": "images/algebra3.png"},
                {"titulo": "Fund. del algebra lineal", "autor": "Ron Larson", "imagen": "images/algebra4.png"},
                {"titulo": "Algebra basica", "autor": "David GOnzales Lopez", "imagen": "images/algebra5.png"},
                {"titulo": "Algebra lineal elemental", "autor": "Richard Hill", "imagen": "images/algebra6.png"},
                {"titulo": "Algebra I for dummies", "autor": "Mary Jane Sterling", "imagen": "images/algebra7.png"},
                {"titulo": "Algebra II for dummies", "autor": "Mary Jane Sterling", "imagen": "images/algebra8.png"},
            ],
        },
        {
            "id": "analisis",
            "titulo": "Análisis Matemático",
            "libros": [
                {"titulo": "Calculo I", "autor": "James Stewart", "imagen": "images/analisis1.png"},
                {"titulo": "Analisis Matematico I", "autor": "Tebar FLores", "imagen": "images/analisis2.png"},
                {"titulo": "Analisis Real y complejo", "autor": "Walter Rudin", "imagen": "images/analisis3.png"},
                {"titulo": "Calculo Avanzado", "autor": "Tom Apostol", "imagen": "images/analisis4.png"},
                {"titulo": "Introduccion al Analisis", "autor": "Richard Johnson", "imagen": "images/analisis5.png"},
                {"titulo": "Geometria analitica", "autor": "LEHMANN", "imagen": "images/analisis6.png"},
                {"titulo": "Ecuaciones diferenciales", "autor": "Takeuchi, Ramirez, Ruiz", "imagen": "images/analisis7.png"},
                {"titulo": "909 problemas de calculo integral", "autor": "E. Tebar Flores", "imagen": "images/analisis8.png"},
            ],
        },
        {
            "id": "ids",
            "titulo": "Introduccion al desarrollo de software",
            "libros": [
                {"titulo": "Bash Guide for Beginners", "autor": "Machtelt Garrels", "imagen": "images/ids1.png"},
                {"titulo": "Linux programing for dummies", "autor": "Jim Keogh", "imagen": "images/ids2.png"},
                {"titulo": "Communicating the User Experience", "autor": "Richard Caddick, Steve Cable", "imagen": "images/ids3.png"},
                {"titulo": "Linux Basics for hackers", "autor": "occupytheweb", "imagen": "images/ids4.png"},
                {"titulo": "Test Driven Development", "autor": "Kent Beck", "imagen": "images/ids5.png"},
                {"titulo": "HTML & CSS", "autor": "Thomas A. Powell", "imagen": "images/ids6.png"},
                {"titulo": "Dominando JavaScript", "autor": "Carlos Azaustre", "imagen": "images/ids7.png"},
                {"titulo": "Building Web Apps with Python and Flask", "autor": " Malhar Lathkar", "imagen": "images/ids8.png"},
            ],
        },
        {
            "id": "funda",
            "titulo": "Fundamentos de programacion",
            "libros": [
                {"titulo": "El lenguaje de programacion C", "autor": " Brian W. Kernighan,  Dennis M. Ritchie", "imagen": "images/funda1.png"},
                {"titulo": "Python a fondo", "autor": "Oscar Ramirez Jimenez", "imagen": "images/funda2.png"},
                {"titulo": "Lenguaje Ensamblador", "autor": "Casella & Berger", "imagen": "images/funda3.png"},
                {"titulo": "Java como programar", "autor": "Deitel", "imagen": "images/funda4.png"},
                {"titulo": "Fundamentos de programacion PHP", "autor": "Ricardo Marcelo", "imagen": "images/funda5.png"},
                {"titulo": "FUndamentos de programacion XML", "autor": "Dave Mercer", "imagen": "images/funda6.png"},
                {"titulo": "El gran libro de programacion en C++", "autor": "Alfonso GOnzales Perez", "imagen": "images/funda7.png"},
                {"titulo": "Aprende python en menos de una semana", "autor": "R.M Lewis", "imagen": "images/funda8.png"},
            ],
        },
    ]
    return render_template("biblioteca.html", materias=materias)

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
