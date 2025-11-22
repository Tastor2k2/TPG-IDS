from flask import Blueprint, jsonify, request
from db import get_connection


carga_libros_bp = Blueprint("carga_libros", __name__)

"""
carga un libro en la db del usuario
"""
@carga_libros_bp.route('/cargar', methods=['POST'])
def cargar_libro():

    
    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')
    codigo_isbn = data.get('codigo_isbn') or data.get('isbn')
    usuario_id = data.get("usuario_id")
    editorial = data.get('editorial')
    tematica = data.get('tematica')


   
    if not titulo or not autor or not codigo_isbn or not usuario_id or not editorial or not tematica:
        return jsonify({
            "error": "Faltan campos obligatorios: titulo, autor, codigo_isbn, usuario_id, editorial, tematica"
        }), 400
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id FROM datos_usuario WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
    

        cursor.execute(
            """INSERT INTO libros 
            (titulo, autor, codigo_isbn, usuario_id, editorial, tematica, estado_del_libro) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (titulo, autor, codigo_isbn, usuario_id, editorial, tematica, 'disponible')
        )

        conn.commit()
        libro_id = cursor.lastrowid

        return jsonify({
            "message": "Libro cargado correctamente",
            "libro_id": libro_id,
            "libro": {
                "id": libro_id,
                "titulo": titulo,
                "autor": autor,
                "codigo_isbn": codigo_isbn,
                "editorial": editorial,
                "tematica": tematica,
                "estado": "disponible",
            }
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Error al cargar el libro: {str(e)}"}), 500
    
    finally:
        cursor.close()
        conn.close()



"""
Obtiene todos los libros de un usuario específico
y los retorna en orden descendente segun su fecha de carga a la pagina
"""
@carga_libros_bp.route('/mis-libros/<int:usuario_id>', methods=['GET'])
def obtener_libros(usuario_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM libros WHERE usuario_id = %s ORDER BY fecha_carga DESC ", (usuario_id,))

        libros = cursor.fetchall()
        
        return jsonify({
            "usuario_id": usuario_id,
            "total_libros": len(libros),
            "libros": libros
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al obtener libros: {str(e)}"}), 500
    
    finally:
        cursor.close()
        conn.close()



"""
Elimina un libro (solo si está en estado 'disponible')
"""
@carga_libros_bp.route('/eliminar/<int:libro_id>', methods=['DELETE'])
def eliminar_libro(libro_id):

    data = request.get_json()
    usuario_id = data.get('usuario_id')
    
    if not usuario_id:
        return jsonify({"error": "Se requiere usuario_id"}), 400
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "SELECT * FROM libros WHERE id = %s AND usuario_id = %s",
            (libro_id, usuario_id)
        )

        libro = cursor.fetchone()
        
        if not libro:
            return jsonify({"error": "Libro no encontrado o no te pertenece"}), 404
        
        if libro['estado_del_libro'] != 'disponible':
            return jsonify({
                "error": f"No se puede eliminar. El libro está en estado: {libro['estado_del_libro']}"
            }), 400
        
        cursor.execute("DELETE FROM libros WHERE id = %s", (libro_id,))
        conn.commit()
        
        return jsonify({
            "message": "Libro eliminado correctamente",
            "libro_id": libro_id,
            "usuario_id": usuario_id,
            "titulo": libro['titulo']
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Error al eliminar: {str(e)}"}), 500
    
    finally:
        cursor.close()
        conn.close()
