from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, send_from_directory
import requests

biblioteca_bp = Blueprint("biblioteca_bp", __name__)

@biblioteca_bp.route('/')
def biblioteca():
    title = "Biblioteca"
    BACK_URL = current_app.config["BACK_URL"]
    URL_BACK_IMAGEN = BACK_URL + "/static/images/"
    # Llamar al BACK
    respuesta_back = requests.get(f"{BACK_URL}/libros/libros")

    if respuesta_back.status_code != 200:
        return render_template("biblioteca.html", libros=[],titulo=title)

    data = respuesta_back.json()
    libros = data.get("libros", [])

    return render_template("biblioteca.html", libros=libros, URL_BACK_IMAGEN=URL_BACK_IMAGEN,titulo=title)