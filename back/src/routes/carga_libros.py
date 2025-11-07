from flask import Blueprint, jsonify, request
from src.db import get_connection

carga_libros_bp  = Blueprint("libros", __name__)

@carga_libros_bp.route('/usuarios', methods=['POST'])
def cargar_libro():

    data = request.get_json() or {}
    titulo = data.get('titulo')
    autor = data.get('autor')
    codigo_isbn = data.get('codigo_isbn') or data.get('isbn')
    usuario_id = data.get('usuario_id') or data.get('id_usuario')

    if not titulo or not autor or not codigo_isbn or not usuario_id:
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM datos WHERE id = %s", (usuario_id,))
    usuario = cursor.fetchone()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 400

    # evitar duplicados por mismo ISBN y usuario
    cursor.execute(
        "SELECT id FROM libros WHERE codigo_isbn = %s AND usuario_id = %s",
        (codigo_isbn, usuario_id)
    )

    if cursor.fetchone():
        return jsonify({"error": "El libro ya existe para este usuario"}), 400

    cursor.execute(
        "INSERT INTO libros (titulo, autor, codigo_isbn, usuario_id) VALUES (%s, %s, %s, %s)",
        (titulo, autor, codigo_isbn, usuario_id)
    )

    conn.commit()
    
    # se asigna a libro_id el id del ultimo registro insertado por el cursor
    libro_id = getattr(cursor, "lastrowid", None)

    cursor.close()
    conn.close()

    return jsonify({"message": "Libro cargado correctamente", "libro_id": libro_id}), 201
    
    