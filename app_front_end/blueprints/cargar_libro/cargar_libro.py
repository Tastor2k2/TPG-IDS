from flask import Blueprint, render_template, request, session, redirect, url_for, current_app,jsonify
import requests

cargar_libro_bp = Blueprint("cargar_libro_bp", __name__)

@cargar_libro_bp.route("/", methods=["GET", "POST"])
def cargar_libro():
    """
    Propósito:
      - Permitir que un usuario logeado cree un nuevo libro y suba su imagen.

    Comportamiento:
      - Requiere sesión: si no existe session["user_id"], redirige a iniciar sesión.
      - Si es GET: renderiza el formulario "cargar_libro.html".
      - Si es POST:
          1) Lee campos del form: titulo, autor, editorial, codigo_isbn, tematica
             y el archivo "imagen".
          2) Valida presencia sin hay titulo, editorial, codigo_isbn, tematica.
             Si faltan, retorna error 400.
          3) Envía datos al backend (POST {BACK_URL}/libros/cargar, JSON)
             incluyendo usuario_id de la sesión. Espera JSON con {"libro_id": ...}.
          4) Con el libro_id, sube la imagen al backend (POST multipart a
             {BACK_URL}/libros/<libro_id>/subir_imagen).
          5) Si la subida de imagen falla (status != 200), retorna 500 indicando
             que el libro se creó pero la imagen no se guardó.
          6) Si todo OK, redirige al perfil del usuario (perfil_bp.perfil).

    Dependencias:
      - app.config["BACK_URL"] definido.
      - Template "templates/cargar_libro.html".
      - Backend con endpoints:
          * POST /libros/cargar -> JSON {"libro_id": int}
          * POST /libros/<libro_id>/subir_imagen (multipart)

    Retornos:
      - GET: HTML del formulario.
      - POST OK: redirect al perfil del usuario.
      - Errores: JSON {"error": "..."} con HTTP 400/500 según corresponda.
    """
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
    if not titulo or not autor or not editorial or not isbn or not tematica or not imagen:
        return jsonify({"error": "Faltan datos"}), 400

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

    # 'imagen' = (nombre de archivo, stream binario, tipo MIME (estándar que identifica el formato de un archivo))
    files = {
        "imagen": (imagen.filename, imagen.stream, imagen.mimetype)
    }

    envio_imagen_back = requests.post(
        f"{BACK_URL}/libros/{libro_id}/subir_imagen",
        files=files
    )
    if envio_imagen_back.status_code != 200:
        return jsonify({"error": "Libro creado pero error al subir imagen"}), 500

    return redirect(url_for("perfil_bp.perfil", id_usuario=session["user_id"]))
