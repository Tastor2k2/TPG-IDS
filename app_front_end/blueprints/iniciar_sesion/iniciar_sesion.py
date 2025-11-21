from flask import Blueprint,render_template,request,redirect,url_for,jsonify,current_app,session
import requests
iniciar_sesion_bp = Blueprint("iniciar_sesion_bp",__name__)

@iniciar_sesion_bp.route("/",methods=["GET","POST"])
def iniciar_sesion():
    BACK_URL = current_app.config['BACK_URL']
    title="Iniciar sesión"
    if request.method == 'POST':
        usuario_o_mail = request.form.get('usuario_o_mail')
        contrasena = request.form.get('contrasena_usuario')

        if not usuario_o_mail or not contrasena:
            return jsonify({"404":"Los campos deben ser completados"}),404
        data = {"email_nombre_usuario": usuario_o_mail,"contraseña": contrasena}
        response = requests.post(f"{BACK_URL}/datos/login", json=data)

        if response.status_code == 200:
            datos = response.json()["usuario"]

            # Guardamos la sesión
            session["user_id"] = datos["id"]
            session["nombre"] = datos["nombre"]
            session["email"] = datos["email"]

            # Redirigimos al perfil
            return redirect(url_for("perfil_bp.perfil", id_usuario=session["user_id"]))
    return render_template('iniciar_sesion.html',titulo=title)
