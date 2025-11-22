from flask import Blueprint, jsonify, request
from db import get_connection


listar_libros_bp = Blueprint("listar_libros", __name__)

"""
Devuelve todos los libros disponibles para intercambio (de todos los usuarios)
Excluye los libros del propio usuario solicitante
"""
@listar_libros_bp.route('/libros', methods=['GET'])
def listar_libros():
    #Obtener usuario_id opcional para excluir sus propios libros
    usuario_id = request.args.get('usuario_id', type=int)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if usuario_id:
            #Excluir libros del propio usuario
            cursor.execute("SELECT * FROM libros WHERE estado_del_libro = 'disponible' AND usuario_id != %s", (usuario_id,))
        else:
            #Mostrar todos los disponibles
            cursor.execute("SELECT * FROM libros WHERE estado_del_libro = 'disponible'")

        libros = cursor.fetchall()

        #muestra todas las imagenes del los libros
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
Devuelve detalles de un libro específico
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