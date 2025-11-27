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
        cursor.execute("""
            SELECT id, titulo, autor, editorial, codigo_isbn, tematica, imagen, fecha_carga, estado_del_libro
            FROM libros
            WHERE usuario_id = %s AND estado_del_libro != 'eliminado'
            ORDER BY fecha_carga DESC
        """, (usuario_id,))

        libros = cursor.fetchall()

        for libro in libros:
            libro["imagen_url"] = f"/static/images/{libro['imagen']}" if libro["imagen"] else None

        return jsonify({
            "usuario_id": usuario_id,
            "total_libros": len(libros),
            "libros": libros
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

"""
Elimina el libro seleccionado por el usuario siempre que sea uno disponible.
Eventualmente si ese libro fue solicitado en un intercambio, se cancelaran todos los intercambios hacia
ese libro y esos quedarán disponibles de nuevo para usarse.
"""
@carga_libros_bp.route('/eliminar', methods=['PATCH'])
def eliminar_libro():
    data = request.get_json()
    id_libro = data.get('id')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, usuario_id, estado_del_libro FROM libros WHERE id = %s", (id_libro,))
        libro = cursor.fetchone()

        if libro['estado_del_libro'] != 'disponible':
            return jsonify({"error": "Solo se pueden eliminar libros en estado disponible"}), 400
        
        cursor.execute("""
            UPDATE libros 
            SET estado_del_libro = 'disponible' 
            WHERE id IN (
                SELECT id_libro_ofrecido 
                FROM intercambio_libro 
                WHERE id_libro_solicitado = %s 
                AND estado_del_intercambio = 'espera'
            )
            AND estado_del_libro = 'pausa'
        """, (id_libro,))
        
        cursor.execute("""
            UPDATE libros 
            SET estado_del_libro = 'disponible' 
            WHERE id IN (
                SELECT id_libro_solicitado 
                FROM intercambio_libro 
                WHERE id_libro_ofrecido = %s 
                AND estado_del_intercambio = 'espera'
            )
            AND estado_del_libro = 'pausa'
        """, (id_libro,))
        
        cursor.execute("""
            UPDATE intercambio_libro 
            SET estado_del_intercambio = 'cancelado', fecha_final = NOW() 
            WHERE (id_libro_ofrecido = %s OR id_libro_solicitado = %s)
            AND estado_del_intercambio = 'espera'
        """, (id_libro, id_libro))
        
        cursor.execute("UPDATE libros SET estado_del_libro = 'eliminado' WHERE id = %s", (id_libro,))
        
        conn.commit()
        return jsonify({"message": "Libro eliminado y todos los intercambios relacionados han sido cancelados"}), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
        
    finally:
        cursor.close()
        conn.close()

  
