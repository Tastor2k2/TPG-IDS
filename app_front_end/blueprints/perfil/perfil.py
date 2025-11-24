from flask import Blueprint, render_template, request, session, jsonify, current_app, redirect, url_for
import requests

perfil_bp = Blueprint("perfil_bp", __name__)

@perfil_bp.route("/usuario/<int:id_usuario>", methods=["GET", "POST"])
def perfil(id_usuario):

    # PROTECCIÓN
    if "user_id" not in session:
        return jsonify({401: "Debes iniciar sesión"}), 401

    if session["user_id"] != id_usuario:
        return jsonify({403: "Acceso no autorizado"}), 403

    BACK_URL = current_app.config["BACK_URL"]
    id_usuario = session["user_id"]

    if request.method == "POST":

        accion = request.form.get("accion")
        codigo = request.form.get("codigo_intercambio")

        if not accion or not codigo:
            return jsonify({"error": "Datos insuficientes"}), 400

        if accion == "aceptar":
            requests.post(
                f"{BACK_URL}/libros/aceptar_intercambio",
                json={"codigo_intercambio": codigo}
            )

        elif accion == "cancelar":
            requests.post(
                f"{BACK_URL}/libros/cancelar_intercambio",
                json={"codigo_intercambio": codigo, "usuario_id": id_usuario}
            )

        # Volver al perfil para ver cambios
        return redirect(url_for("perfil_bp.perfil", id_usuario=id_usuario))

    respuesta_back = requests.post(
        f"{BACK_URL}/libros/intercambios/historial/{id_usuario}"
    )

    if respuesta_back.status_code != 200:
        historial = {"pendientes": [], "completados": [], "cancelados": []}
    else:
        historial = respuesta_back.json()

    return render_template(
        "perfil.html",
        nombre=session["nombre"],
        email=session["email"],
        id=id_usuario,
        historial=historial
    )
