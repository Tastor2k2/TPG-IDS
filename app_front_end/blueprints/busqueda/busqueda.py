from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
import requests

busqueda_bp = Blueprint("busqueda_bp", __name__)

@busqueda_bp.route("/", methods=["GET"])
def busqueda():

    # obligar a iniciar sesión
    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    BACK_URL = current_app.config["BACK_URL"]
    search = request.args.get("search", "").strip()
    id_usuario = session["user_id"]

    if not search:
        return render_template("busqueda.html", libros=[], search="")

    peticion_back = requests.get(
        f"{BACK_URL}/libros/buscar",
        params={
            "search": search,
            "usuario_id": id_usuario
        }
    )

    libros = []
    if peticion_back.status_code == 200:
        libros = peticion_back.json().get("libros", [])

    return render_template(
        "busqueda.html",
        libros=libros,
        search=search,
        url_back = BACK_URL
    )
