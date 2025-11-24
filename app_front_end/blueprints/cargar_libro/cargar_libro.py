from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import requests

cargar_libro_bp = Blueprint("cargar_libro_bp", __name__)

@cargar_libro_bp.route("/", methods=["GET", "POST"])
def cargar_libro():

    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    if request.method == "GET":
        return render_template("cargar_libro.html")

    # DATOS DEL LIBRO
    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    editorial = request.form.get("editorial")
    isbn = request.form.get("codigo_isbn")
    tematica = request.form.get("tematica")
    imagen = request.files.get("imagen")

    # Validación básica
    if not titulo or not editorial or not isbn or not tematica:
        return {"error": "Faltan datos"}, 400

    BACK_URL = current_app.config["BACK_URL"]

    data_json = {
        "titulo": titulo,
        "autor": autor,
        "editorial": editorial,
        "codigo_isbn": isbn,
        "tematica": tematica,
        "usuario_id": session["user_id"]
    }

    # Enviar JSON
    envio_info_back = requests.post(
        f"{BACK_URL}/libros/cargar",
        json=data_json
    )

    libro_id = envio_info_back.json()["libro_id"]

    files = {
        "imagen": (imagen.filename, imagen.stream, imagen.mimetype)
    }

    envio_imagen_back = requests.post(
        f"{BACK_URL}/libros/{libro_id}/subir_imagen",
        files=files
    )
    print("STATUS IMAGEN:", envio_imagen_back.status_code)
    print("RESPUESTA IMAGEN:", envio_imagen_back.text)
    if envio_imagen_back.status_code != 200:
        return {"error": "Libro creado pero error al subir imagen"}, 500

    return redirect(url_for("perfil_bp.perfil", id_usuario=session["user_id"]))
