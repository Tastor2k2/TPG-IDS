from flask import Blueprint, url_for,request,redirect,render_template,jsonify,current_app
import requests
registrarse_bp = Blueprint("registrarse_bp",__name__)

@registrarse_bp.route('/',methods=['GET','POST'])
def registrarse():
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
            return jsonify({"error": "Faltan campos por rellenar"}),400
        if  (mail != mail_confirmacion):
            return jsonify({"error": "Los mails no coinciden"}),400
        data = {"nombre":usuario,"email":mail,"contraseña":contrasena,"telefono_usuario":telefono,
                "direccion_usuario":direccion,"dni_usuario":dni}
        requests.post(f"{BACK_URL}/datos/registrar", json=data)
    return redirect(url_for('index',user=usuario,email=mail,mail_conf=mail_confirmacion,password=contrasena))
