from flask import Blueprint, url_for,request,redirect,render_template

registrarse_bp = Blueprint("registrarse_bp",__name__)

@registrarse_bp.route('/',methods=['GET','POST'])
def registrarse():
    title="Registrarse"
    if request.method == 'POST':
        usuario = request.form.get('nombre_usuario')
        mail = request.form.get('email_registro')
        mail_confirmacion = request.form.get('email_confirmacion')
        contrasena = request.form.get('contrasena_registro')
        #insertar_usuario(usuario,mail,contrasena)
        return redirect(url_for('index',user=usuario,email=mail,mail_conf=mail_confirmacion,password=contrasena))
    return render_template('registrarse.html',titulo=title)
