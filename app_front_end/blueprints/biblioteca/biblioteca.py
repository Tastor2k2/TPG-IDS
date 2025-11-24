from flask import Blueprint, render_template, session, current_app
import requests

biblioteca_bp = Blueprint("biblioteca_bp", __name__)

@biblioteca_bp.route('/')
def biblioteca():
    """
    Vista de la sección Biblioteca.

    Propósito:
      - Mostrar la biblioteca filtrada para el usuario logueado.

    Flujo:
      1) Define el título de la página.
      2) Lee la URL del backend desde app.config['BACK_URL'] y arma el prefijo de imágenes (BACK_URL + "/static/images/").
      3) Toma el id de usuario desde la sesión (session.get("user_id")).
      4) Llama al backend: GET {BACK_URL}/libros/libros?usuario_id=<id_usuario>.
         - Se espera JSON con la forma: {"libros": [...] }.
      5) Si la respuesta no es 200 (la solicitud NO se procesó bien), renderiza la plantilla con lista vacía.
      6) Si es exitosa, extrae "libros" del JSON y renderiza la plantilla "biblioteca.html"
         enviando: libros, URL_BACK_IMAGEN y titulo.

    Requisitos:
      - app.config['BACK_URL'] configurado.
      - Templates 'biblioteca.html' existente.

    Parámetros:
      - Ninguno, debido a que usa sesión y configuración global.

    Retorna:
      - Template renderizado (200 OK) con la biblioteca del usuario
        o con lista vacía si el backend no responde 200.
    """
    title = "Biblioteca"
    BACK_URL = current_app.config["BACK_URL"]
    URL_BACK_IMAGEN = BACK_URL + "/static/images/"

    # OBTENER ID DEL USUARIO LOGUEADO
    id_usuario = session.get("user_id")

    # LLAMADA AL BACK: FILTRA LIBROS DEL USUARIO
    respuesta_back = requests.get(
        f"{BACK_URL}/libros/libros",
        params={"usuario_id": id_usuario}
    )

    if respuesta_back.status_code != 200:
        return render_template("biblioteca.html", libros=[], titulo=title)

    data = respuesta_back.json()
    libros = data.get("libros", [])

    return render_template(
        "biblioteca.html",
        libros=libros,
        URL_BACK_IMAGEN=URL_BACK_IMAGEN,
        titulo=title
    )
