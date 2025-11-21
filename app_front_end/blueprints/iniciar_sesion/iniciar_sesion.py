from flask import Blueprint,render_template,request,redirect,url_for

iniciar_sesion_bp = Blueprint("iniciar_sesion_bp",__name__)

@iniciar_sesion_bp.route("/",methods=["GET","POST"])
def iniciar_sesion():
    title="Iniciar sesión"
    if request.method == 'POST':
        mail = request.form.get('email_usuario')
        contrasena = request.form.get('contrasena_usuario')
        if not mail or not contrasena:
            return "Volver a pedir"
        return redirect(url_for('index',email=mail,password=contrasena))
    return render_template('iniciar_sesion.html',titulo=title)
