from flask import Blueprint, render_template, session, redirect, url_for, current_app
import requests

intercambio_bp = Blueprint("intercambio_bp", __name__)

@intercambio_bp.route('/')
def intercambio():
    # Checkea que esté loguado
    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))
    
    id_usuario = session["user_id"]
    BACK_URL = current_app.config["BACK_URL"]
    respuesta_back = requests.get(f"{BACK_URL}/libros/mis-libros/{id_usuario}")
    libros = []
    if respuesta_back.status_code == 200:
        libros = respuesta_back.json().get("libros", [])

    cantidad_libros = len(libros)
    # Si no tiene libros, lo manda a cargar
    if cantidad_libros == 0:
        return redirect(url_for('cargar_libro_bp.cargar_libro'))
    
    return render_template("intercambio.html",libros=libros)