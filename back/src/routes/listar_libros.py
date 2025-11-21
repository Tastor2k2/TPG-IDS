from flask import Blueprint, jsonify, request
from db import get_connection


listar_libros_bp = Blueprint("listar_libros", __name__)

"""
Devuelve todos los libros disponibles para intercambio (de todos los usuarios)
Excluye los libros del propio usuario solicitante
"""
@listar_libros_bp.route('/libros', methods=['GET'])
def listar_libros():
    #check = validar_sesion()
    #if check: return check
    """
    JSON de entrada: Query params opcionales
    URL: /libros?usuario_id=1 (opcional, para excluir libros propios)
    
    JSON de salida (respuesta exitosa):
    {
        "total_libros": 10,
        "libros": [
            {
                "id": 3,
                "usuario_id": 2,
                "titulo": "El Principito",
                "autor": "Saint-Exupéry",
                "codigo_isbn": "9788478887194",
                "editorial": "Salamandra",
                "tematica": "Infantil",
                "estado_del_libro": "disponible",
                "es_favorito": false
            }
        ]
    }
    """
    # Obtener usuario_id opcional para excluir sus propios libros
    usuario_id = request.args.get('usuario_id', type=int)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if usuario_id:
            # Excluir libros del propio usuario
            cursor.execute(
                """SELECT id, usuario_id, titulo, autor, codigo_isbn, editorial, 
                tematica, estado_del_libro, es_favorito 
                FROM libros 
                WHERE estado_del_libro = 'disponible' AND usuario_id != %s""",
                (usuario_id,)
            )
        else:
            # Mostrar todos los disponibles
            cursor.execute(
                """SELECT id, usuario_id, titulo, autor, codigo_isbn, editorial, 
                tematica, estado_del_libro, es_favorito 
                FROM libros 
                WHERE estado_del_libro = 'disponible'"""
            )
        
        libros = cursor.fetchall()
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
    #check = validar_sesion()
    #if check: return check
    """
    JSON de entrada: No requiere body (usa parámetro de URL)
    URL: /libros/5
    
    JSON de salida (respuesta exitosa):
    {
        "id": 5,
        "usuario_id": 2,
        "titulo": "1984",
        "autor": "George Orwell",
        "codigo_isbn": "1122334455",
        "editorial": "Debolsillo",
        "tematica": "Distopía",
        "estado_del_libro": "disponible",
        "es_favorito": true,
        "fecha_carga": "2025-11-10 09:15:00"
    }
    """
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