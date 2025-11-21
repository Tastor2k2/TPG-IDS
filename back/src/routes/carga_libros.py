from flask import Blueprint, jsonify, request
from db import get_connection

carga_libros_bp = Blueprint("carga_libros", __name__)

"""
carga un libro en la db del usuario
"""
@carga_libros_bp.route('/cargar', methods=['POST'])
def cargar_libro():
    if check: return check
    """
    JSON de entrada esperado:
    {
        "titulo": "El Quijote",
        "autor": "Cervantes",
        "codigo_isbn": "1234567890",
        "usuario_id": 1,
        "editorial": "Planeta",
        "tematica": "Novela",
        "es_favorito": false
    }

    JSON de salida (respuesta exitosa):
    {
        "message": "Libro cargado correctamente",
        "libro_id": 1,
        "libro": {
            "id": 1,
            "titulo": "El Quijote",
            "autor": "Cervantes",
            "codigo_isbn": "1234567890",
            "editorial": "Planeta",
            "tematica": "Novela",
            "estado": "disponible",
            "es_favorito": false
        }
    }
    """
    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')
    codigo_isbn = data.get('codigo_isbn') or data.get('isbn')
    usuario_id = session.get("usuario_id")
    editorial = data.get('editorial')
    tematica = data.get('tematica')
    es_favorito = data.get('es_favorito', False)

    

    if not titulo or not autor or not codigo_isbn or not usuario_id or not editorial or not tematica or es_favorito is None:
        return jsonify({
            "error": "Faltan campos obligatorios: titulo, autor, codigo_isbn, usuario_id, editorial, tematica, es_favorito"
        }), 400
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id FROM datos_usuario WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        cursor.execute(
            "SELECT id FROM libros WHERE codigo_isbn = %s AND usuario_id = %s",
            (codigo_isbn, usuario_id)
        )

        if cursor.fetchone():
            return jsonify({"error": "Ya tienes este libro registrado (mismo ISBN)"}), 409

        cursor.execute(
            """INSERT INTO libros 
            (titulo, autor, codigo_isbn, usuario_id, editorial, tematica, estado_del_libro, es_favorito) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (titulo, autor, codigo_isbn, usuario_id, editorial, tematica, 'disponible', es_favorito)
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
                "es_favorito": es_favorito
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
    """
    JSON de entrada: No requiere body (usa parámetro de URL)
    URL: /mis-libros/1
    
    JSON de salida (respuesta exitosa):
    {
        "usuario_id": 1,
        "total_libros": 5,
        "libros": [
            {
                "id": 1,
                "titulo": "El Quijote",
                "autor": "Cervantes",
                "codigo_isbn": "1234567890",
                "editorial": "Planeta",
                "tematica": "Novela",
                "estado_del_libro": "disponible",
                "es_favorito": false,
                "fecha_carga": "2025-11-13 10:30:00"
            },
            {
                "id": 2,
                "titulo": "Cien años de soledad",
                "autor": "García Márquez",
                "codigo_isbn": "0987654321",
                "editorial": "Sudamericana",
                "tematica": "Realismo mágico",
                "estado_del_libro": "disponible",
                "es_favorito": true,
                "fecha_carga": "2025-11-12 15:20:00"
            }
        ]
    }
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            """SELECT id, titulo, autor, codigo_isbn, editorial, tematica, 
            estado_del_libro, es_favorito, fecha_carga 
            FROM libros WHERE usuario_id = %s 
            ORDER BY fecha_carga DESC""",
            (usuario_id,)
        )

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
Obtiene solo los libros marcados como favoritos de un usuario
y los retorna en orden descendente segun su fecha de carga a la pagina
"""
@carga_libros_bp.route('/favoritos/<int:usuario_id>', methods=['GET'])
def obtener_favoritos(usuario_id):
    """
    JSON de entrada: No requiere body (usa parámetro de URL)
    URL: /favoritos/1
    
    JSON de salida (respuesta exitosa):
    {
        "usuario_id": 1,
        "total_favoritos": 2,
        "favoritos": [
            {
                "id": 2,
                "titulo": "Cien años de soledad",
                "autor": "García Márquez",
                "codigo_isbn": "0987654321",
                "editorial": "Sudamericana",
                "tematica": "Realismo mágico",
                "estado_del_libro": "disponible",
                "es_favorito": true,
                "fecha_carga": "2025-11-12 15:20:00"
            },
            {
                "id": 5,
                "titulo": "1984",
                "autor": "George Orwell",
                "codigo_isbn": "1122334455",
                "editorial": "Debolsillo",
                "tematica": "Distopía",
                "estado_del_libro": "disponible",
                "es_favorito": true,
                "fecha_carga": "2025-11-10 09:15:00"
            }
        ]
    }
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            """SELECT id, titulo, autor, codigo_isbn, editorial, tematica, 
            estado_del_libro, es_favorito, fecha_carga 
            FROM libros WHERE usuario_id = %s AND es_favorito = TRUE
            ORDER BY fecha_carga DESC""",
            (usuario_id,)
        )
        favoritos = cursor.fetchall()
        
        return jsonify({
            "usuario_id": usuario_id,
            "total_favoritos": len(favoritos),
            "favoritos": favoritos
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al obtener favoritos: {str(e)}"}), 500
    
    finally:
        cursor.close()
        conn.close()

"""
Marca o desmarca unn libro como favorito
"""
@carga_libros_bp.route('/marcar-favorito/<int:libro_id>', methods=['PUT'])
def marcar_favorito(libro_id):
    """
    JSON de entrada esperado:
    {
        "usuario_id": 1,
        "es_favorito": true o false
    }
    
    JSON de salida (respuesta exitosa):
    {
        "message": "Libro agregado a favoritos",
        "libro_id": 5,
        "es_favorito": true
    }
    
    O si se desmarca:
    {
        "message": "Libro quitado de favoritos",
        "libro_id": 5,
        "es_favorito": false
    }
    """
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    es_favorito = data.get('es_favorito')
    
    if not usuario_id or es_favorito is None:
        return jsonify({"error": "Se requiere usuario_id y es_favorito (true/false)"}), 400
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "SELECT id FROM libros WHERE id = %s AND usuario_id = %s",
            (libro_id, usuario_id)
        )
        
        if not cursor.fetchone():
            return jsonify({"error": "Libro no encontrado o no te pertenece"}), 404
        
        cursor.execute(
            "UPDATE libros SET es_favorito = %s WHERE id = %s",
            (es_favorito, libro_id)
        )
        conn.commit()
        
        mensaje = "agregado a" if es_favorito else "quitado de"
        return jsonify({
            "message": f"Libro {mensaje} favoritos",
            "libro_id": libro_id,
            "es_favorito": es_favorito
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Error al actualizar favorito: {str(e)}"}), 500
    
    finally:
        cursor.close()
        conn.close()

"""
Elimina un libro (solo si está en estado 'disponible')
"""
@carga_libros_bp.route('/eliminar/<int:libro_id>', methods=['DELETE'])
def eliminar_libro(libro_id):
    """
    JSON de entrada esperado:
    {
        "usuario_id": 1
    }
    JSON de salida (respuesta exitosa):
    {
        "message": "Libro eliminado correctamente",
        "libro_id": 1,
        "usuario_id": 1,
        "titulo": "El Quijote"
    }
    """
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
