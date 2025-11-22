import os
from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, request
from db import get_connection


carga_libros_imagenes_bp = Blueprint("carga_libros_imagenes", __name__)

UPLOAD_FOLDER = "static/images"

def allowed_file(filename):
    ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@carga_libros_imagenes_bp.route("/<int:libro_id>/subir_imagen", methods=["POST"])
def subir_imagen(libro_id):
    imagen = request.files["imagen"]

    if not imagen:
        return jsonify({"error": "No se envió imagen"}), 400

    if imagen.filename == "":
        return jsonify({"error": "Nombre de archivo inválido"}), 400

    if not allowed_file(imagen.filename):
        return jsonify({"error": "Formato no permitido"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(f"libro_{libro_id}_" + imagen.filename)
    ruta = os.path.join(UPLOAD_FOLDER, filename)

    imagen.save(ruta)

    # Guardar nombre en la DB
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    #chequeamos si existe el libro
    cursor.execute("SELECT id FROM libros WHERE id=%s", (libro_id,))
    libro = cursor.fetchone()

    #si no existe
    if not libro:
        cursor.close()
        conn.close()
        return jsonify({"error": "Libro no encontrado"}), 404

    #si existe
    cursor.execute("UPDATE libros SET imagen=%s WHERE id=%s", (filename, libro_id))



    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Imagen subida",
        "imagen_url": f"static/images/{filename}"
}), 200
