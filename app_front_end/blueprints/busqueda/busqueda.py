from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
import requests

busqueda_bp = Blueprint("busqueda_bp", __name__)

@busqueda_bp.route("/", methods=["GET"])
def busqueda():
    """
    Propósito:
      - Mostrar resultados de búsqueda de libros para el usuario logueado.

    Flujo:
      1) Verifica sesión: si no existe 'session["user_id"]', redirige a iniciar sesión.
      2) Lee el término 'search' de la barra de busqueda; si viene vacío, renderiza la plantilla sin resultados.
      3) Obtiene 'BACK_URL' de 'app.config' y el 'id_usuario' de la sesión.
      4) Llama al backend: GET {BACK_URL}/libros/buscar con params 'search' e 'usuario_id'.
      5) Si la respuesta es 200, toma 'data["libros"]'. En otro caso, usa lista vacía.
      6) Renderiza 'busqueda.html' pasando: 'libros', 'search' y 'url_back' (BACK_URL).

    Requisitos:
      - 'app.config['BACK_URL']' configurado.
      - Plantilla 'templates/busqueda.html'.
      - Backend que responda JSON con la clave "libros".

    Retorna:
      - Los resultados de la busqueda (o lista vacía).
      - Redirecciona al login si no hay sesión.
    """
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
