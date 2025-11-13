from flask import Blueprint, jsonify
from src.db import get_connection

libros_bp = Blueprint("listar_libros", __name__)

"""Devuelve todos los libros disponibles con sus atributos"""
@libros_bp.route('/libros', methods=['GET'])
def listar_libros():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, usuario_id, titulo, autor, codigo_isbn, estado_del_libro, es_favorito FROM libros WHERE estado_del_libro = 'disponible'")
        libros = cursor.fetchall()
        return jsonify({"libros": libros}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

"""Devuelve detalles de un libro específico"""
@libros_bp.route('/libros/<int:libro_id>', methods=['GET'])
def obtener_libro(libro_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM libros WHERE id = %s", (libro_id,))
        libro = cursor.fetchone()
        if not libro:
            return jsonify({"error": "Libro no encontrado"}), 404
        return jsonify(libro), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()