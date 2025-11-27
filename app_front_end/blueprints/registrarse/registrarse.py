from flask import Blueprint, url_for,request,redirect,render_template,jsonify,current_app
import requests
registrarse_bp = Blueprint("registrarse_bp",__name__)

@registrarse_bp.route('/',methods=['GET','POST'])
def registrarse():
    """
    Propósito:
        - Mostrar el formulario de alta de usuario y enviar los datos al backend para crear la cuenta.

    Flujo:
        GET (no se envia formulario):
            - Renderiza 'registrarse.html' con el título de página.

        POST (se envía form):
            - Lee campos del formulario:
                * nombre_usuario, email_registro, email_confirmacion, contrasena_registro,
                    telefono_usuario, direccion_usuario, dni_usuario.
            - Se validan los campo:
                * Si faltan: usuario, mail, mail_confirmacion o contrasena, se vuelve a renderizar el templete de registrarse.
                * Si mail != mail_confirmacion, se vuelve a renderizar el templete de registrarse.
            - Arma el payload JSON (info en formato JSON que le llega a la DB) con las claves que espera el backend:
            - Envía POST a {BACK_URL}/datos/registrar con ese JSON.
            - Redirige a la home (index_bp.index) tras el intento de registro.

    Dependencias:
        - app.config['BACK_URL'] definido con la URL del backend.
        - Template 'registrarse.html'.
        - Endpoint del backend: POST /datos/registrar que acepte el JSON anterior.

    Retornos:
        - Muestra formulario de registro.
        - Si la registración es exitosa, se redirecciona a la home y se envía al backend la info.
        - Error 400 cuando fallan las validaciones de campos/mails.
    """
    BACK_URL = current_app.config['BACK_URL']
    title="Registrarse"
    if request.method == 'GET':
        return render_template('registrarse.html', titulo=title)
    if request.method == 'POST':
        usuario = request.form.get('nombre_usuario')
        mail = request.form.get('email_registro')
        mail_confirmacion = request.form.get('email_confirmacion')
        contrasena = request.form.get('contrasena_registro')
        telefono = request.form.get('telefono_usuario')
        direccion = request.form.get('direccion_usuario')
        dni = request.form.get('dni_usuario')
        if (not usuario) or (not mail) or (not mail_confirmacion) or (not contrasena):
            return render_template('registrarse.html', titulo=title)
        if  (mail != mail_confirmacion):
            return render_template('registrarse.html', titulo=title)
        data = {"nombre":usuario,"email":mail,"contraseña":contrasena,"telefono_usuario":telefono,
                "direccion_usuario":direccion,"dni_usuario":dni}
        requests.post(f"{BACK_URL}/datos/registrar", json=data)
    return redirect(url_for('index_bp.index'))
