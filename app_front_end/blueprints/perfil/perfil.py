from flask import Blueprint,Flask,render_template,request,session,jsonify

perfil_bp = Blueprint("perfil_bp",__name__)

@perfil_bp.route("/usuario/<int:id_usuario>")
def perfil(id_usuario):
    """
    Redirige al usuario a su perfil.
    PRECONDICION:
        - id_usuario
    POSTCONDICION:
        - 
    """
    # Protección del perfil
    if "user_id" not in session:
        return jsonify({401:"Debes iniciar sesión"}), 401

    if session["user_id"] != id_usuario:
        return jsonify({403:"Acceso no autorizado"}), 403

    # Se muestra el perfil
    return render_template(
        "perfil.html",
        nombre=session["nombre"],
        email=session["email"],
        id=id_usuario
    )