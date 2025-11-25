from flask import Blueprint, render_template, current_app, session, redirect, url_for
import requests

mis_libros_bp = Blueprint("mis_libros_bp", __name__)

@mis_libros_bp.route("/", methods=["GET"])
def mis_libros():
    """
    Propósito:
    Traer desde el backend la lista de libros que pertenecen al usuario logueado
    y renderizar el template 'mis_libros.html'.

    Flujo:
        1) Valida que exista sesión ('session["user_id"]'). Si no, redirige a iniciar sesión.
        2) Lee 'BACK_URL' de la config del app y el 'id_usuario' de la sesión.
        3) Llama al backend: GET {BACK_URL}/libros/mis-libros/<id_usuario>.
        4) Si la respuesta es 200, toma la lista de libros del JSON. Si no, usa lista vacía.
        5) Renderiza el template con:
            - 'libros': lista de libros del usuario.
            - 'URL_BACK_IMAGEN': prefijo para armar URLs de imágenes del back.

    Dependencias:
        - 'app.config["BACK_URL"]' debe estar seteado.
        - Endpoint del back '/libros/mis-libros/<id>' que devuelva JSON con clave "libros".
        - Template 'mis_libros.html'.

    Retorno:
        - El grid de libros del usuario o un mensaje si no hay resultados.
        - Redirección a iniciar sesión si no hay usuario en sesión.
    """
    # Se obliga a iniciar sesion
    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    BACK_URL = current_app.config["BACK_URL"]
    id_usuario = session["user_id"]

    # Llamada al back
    peticion_back = requests.get(f"{BACK_URL}/libros/mis-libros/{id_usuario}")

    libros = []
    # Se almacena en la variable 'libros' lo que se encuentra en la clave json llamada 'libros'
    if peticion_back.status_code == 200:
        libros = peticion_back.json().get("libros", [])

    return render_template(
        "mis_libros.html",
        libros=libros,
        URL_BACK_IMAGEN = BACK_URL
    )
