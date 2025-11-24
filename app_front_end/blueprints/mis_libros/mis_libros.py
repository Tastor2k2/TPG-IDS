from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
import requests

mis_libros_bp = Blueprint("mis_libros_bp", __name__)

@mis_libros_bp.route("/", methods=["GET"])
def mis_libros():

    # obligar a iniciar sesión
    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    BACK_URL = current_app.config["BACK_URL"]
    id_usuario = session["user_id"]

    # LLAMO AL BACK CORRECTO
    peticion_back = requests.get(f"{BACK_URL}/libros/mis-libros/{id_usuario}")

    libros = []
    if peticion_back.status_code == 200:
        libros = peticion_back.json().get("libros", [])

    return render_template(
        "mis_libros.html",
        libros=libros,
        URL_BACK_IMAGEN = BACK_URL
    )
