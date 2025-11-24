from flask import Blueprint,render_template,request,redirect,url_for,jsonify,current_app,session
import requests
iniciar_sesion_bp = Blueprint("iniciar_sesion_bp",__name__)

@iniciar_sesion_bp.route("/",methods=["GET","POST"])
def iniciar_sesion():
    """
    Proposito:
      - Autenticar al usuario contra el backend y establecer sesión en el front.

    Flujo:
      - Si es GET: renderiza 'iniciar_sesion.html' con el título.
      - Si es POST:
          1) Lee 'usuario_o_mail' y 'contrasena_usuario' del formulario.
          2) Si falta alguno, devuelve JSON {"404":"Los campos deben ser completados"} con HTTP 404.
          3) Envía al backend (POST {BACK_URL}/datos/login) un JSON:
               {"email_nombre_usuario": <usuario_o_mail>, "contraseña": <contrasena>}
          4) Si el backend responde 200, extrae 'usuario' del JSON y guarda en sesión:
               session["user_id"], session["nombre"], session["email"].
          5) Redirige al perfil del usuario: url_for("perfil_bp.perfil", id_usuario=session["user_id"]).

    Dependencias:
      - app.config['BACK_URL'] configurado.
      - Template 'iniciar_sesion.html'.
      - Backend: POST /datos/login debe devolver 200 y JSON con clave "usuario" que incluya 'id', 'nombre' y 'email'.

    Retornos:
      - Si es GET, retorna el inicio de sesion.
      - Si  es POST 302 (encontrado): redirección al perfil si login OK.
      - Si es POST 400 (no pudo entender la solicitud): JSON de error si faltan campos.
      - Si el backend no devuelve 200, se vuelve a renderizar el formulario (sin mensaje en este código).
    """
    BACK_URL = current_app.config['BACK_URL']
    title="Iniciar sesión"
    if request.method == 'POST':
        usuario_o_mail = request.form.get('usuario_o_mail')
        contrasena = request.form.get('contrasena_usuario')

        if not usuario_o_mail or not contrasena:
            return jsonify({"400":"Los campos deben ser completados"}),400
        data = {"email_nombre_usuario": usuario_o_mail,"contraseña": contrasena}
        response = requests.post(f"{BACK_URL}/datos/login", json=data)

        if response.status_code == 200:
            datos = response.json()["usuario"]

            # Se guarda la sesión
            session["user_id"] = datos["id"]
            session["nombre"] = datos["nombre"]
            session["email"] = datos["email"]

            # Se redirige al perfil
            return redirect(url_for("perfil_bp.perfil", id_usuario=session["user_id"]))
    return render_template('iniciar_sesion.html',titulo=title)
