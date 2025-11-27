from flask import Blueprint, jsonify, request
from db import get_connection

listar_libros_bp = Blueprint("listar_libros", __name__)

"""
Devuelve todos los libros disponibles para intercambio (de todos los usuarios)
Excluye los libros del propio usuario solicitante
"""
@listar_libros_bp.route('/libros', methods=['GET'])
def listar_libros():

    usuario_id = request.args.get('usuario_id', type=int)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        if usuario_id:
            cursor.execute("SELECT * FROM libros WHERE estado_del_libro = 'disponible' AND usuario_id != %s", (usuario_id,))
        else:
            cursor.execute("SELECT * FROM libros WHERE estado_del_libro = 'disponible'")

        libros = cursor.fetchall()

        for libro in libros:
            libro["imagen_url"] = f"/static/images/{libro['imagen']}"

        return jsonify({
            "total_libros": len(libros),
            "libros": libros
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

"""
Devuelve al front los resultados de la búsqueda de uno o más libros realizada en la barra de búsqueda.
Se puede buscar a través de cualquier parámetro o variable presente en la tabla de los libros dentro de
la base de datos.
"""
@listar_libros_bp.route('/buscar', methods=['GET'])
def buscar_libros():
    search = request.args.get("search", "").strip()
    usuario_id = request.args.get("usuario_id", type=int)

    if usuario_id is None:
        return jsonify({"error": "usuario_id requerido"}), 400

    wildcard = f"%{search}%"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT *
            FROM libros
            WHERE estado_del_libro = 'disponible'
              AND usuario_id != %s
              AND (
                    titulo LIKE %s
                 OR autor LIKE %s
                 OR codigo_isbn LIKE %s
                 OR editorial LIKE %s
                 OR tematica LIKE %s
              )
        """

        cursor.execute(query, (usuario_id, wildcard, wildcard, wildcard, wildcard, wildcard))

        libros = cursor.fetchall()

        for libro in libros:
            libro["imagen_url"] = f"/static/images/{libro['imagen']}"

        return jsonify({
            "total_libros": len(libros),
            "libros": libros
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

"""
Devuelve la información detallada de un libro específico por su ID
"""
@listar_libros_bp.route('/libros/<int:libro_id>', methods=['GET'])
def obtener_libro(libro_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM libros WHERE id = %s", (libro_id,))
        libro = cursor.fetchone()

        if not libro:
            return jsonify({"error": "Libro no encontrado"}), 404
        
        libro["imagen_url"] = f"/static/images/{libro['imagen']}"

        return jsonify(libro), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()  