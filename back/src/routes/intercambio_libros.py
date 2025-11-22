from flask import Blueprint, jsonify, request
from db import get_connection

intercambio_libros_bp  = Blueprint("intercambio_libros", __name__)


"""
Muestra la cantidad total de libros que tiene el usuario
"""
@intercambio_libros_bp.route("/usuarios/<int:usuario_id>/tiene_libros", methods=["GET"])
def tiene_libros(usuario_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT COUNT(*) AS total FROM libros WHERE usuario_id = %s",
            (usuario_id,)
        )
        total = cursor.fetchone()["total"]
        return jsonify({"usuario_id": usuario_id, "total": total, "tiene_libros": total > 0}), 200
    
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500  

    finally:
        cursor.close()
        conn.close() 


"""
Crea una solicitud de intercambio
"""
@intercambio_libros_bp.route('/solicitar_intercambio', methods=['POST'])
def solicitar_intercambio():

    data = request.get_json()
    id_libro_solicitado = data.get('id_libro_solicitado')
    id_libro_ofrecido = data.get('id_libro_ofrecido')
    solicitante_id = data.get('id_usuario_ofrecido')
    solicitado_id = data.get('id_usuario_solicitado')

    if not id_libro_solicitado or not id_libro_ofrecido or not solicitante_id or not solicitado_id:
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, usuario_id, estado_del_libro FROM libros WHERE id = %s", (id_libro_solicitado,))
        libro_solicitado = cursor.fetchone()
        cursor.execute("SELECT id, usuario_id, estado_del_libro FROM libros WHERE id = %s", (id_libro_ofrecido,))
        libro_ofrecido = cursor.fetchone()


        if not libro_solicitado or not libro_ofrecido:
            return jsonify({"error": "No hay un libro por libro para intercambiar, debe haber 1 como mínimo por cada usuario"}), 400

        if id_libro_solicitado == id_libro_ofrecido:
            return jsonify({"error": "No se puede intercambiar el mismo libro"}), 400
        
        if libro_solicitado.get("estado_del_libro") != 'disponible' or libro_ofrecido.get("estado_del_libro") != 'disponible':
            return jsonify({"error": "Ambos libros deben estar en estado 'disponible'"}), 400
        
        id_libro_ofrecido = libro_ofrecido["id"]

        cursor.execute("UPDATE libros SET estado_del_libro = 'pausa' WHERE id = %s", (id_libro_ofrecido,))
        cursor.execute(
                    """
                    INSERT INTO intercambio_libro 
                    (id_libro_solicitado, id_libro_ofrecido, id_usuario_solicitado, id_usuario_ofrecido, estado_del_intercambio)
                    VALUES (%s, %s, %s, %s, 'espera')
                    """,
                    (id_libro_solicitado, id_libro_ofrecido, solicitado_id, solicitante_id)
                )
        conn.commit()
        intercambio_id = cursor.lastrowid

        return jsonify({"message": "Solicitud creada", "codigo_intercambio": intercambio_id}), 201
    
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

"""
Acepta una solicitud de intercambio y lo completa automáticamente.
El propietario del libro solicitado debe aceptar.
"""
@intercambio_libros_bp.route('/aceptar_intercambio', methods=['POST'])
def aceptar_intercambio():
    
    data = request.get_json()
    codigo = data.get('codigo_intercambio')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM intercambio_libro WHERE codigo_intercambio = %s", (codigo,))
        intercambio = cursor.fetchone()
        
        if not intercambio:
            return jsonify({"error": "Intercambio no encontrado"}), 404

        if intercambio.get("estado_del_intercambio") != 'espera':
            return jsonify({
                "error": f"El intercambio no puede aceptarse. Estado actual: {intercambio.get('estado_del_intercambio')}"
            }), 400

        id_libro_solicitado = intercambio["id_libro_solicitado"]
        id_libro_ofrecido = intercambio["id_libro_ofrecido"]
        id_usuario_solicitado = intercambio["id_usuario_solicitado"]
        id_usuario_ofrecido = intercambio["id_usuario_ofrecido"]

        cursor.execute("SELECT id, usuario_id, estado_del_libro FROM libros WHERE id = %s", (id_libro_solicitado,))
        libro_solicitado = cursor.fetchone()
        
        cursor.execute("SELECT id, usuario_id, estado_del_libro FROM libros WHERE id = %s", (id_libro_ofrecido,))
        libro_ofrecido = cursor.fetchone()

        if not libro_solicitado or not libro_ofrecido:
            return jsonify({"error": "Uno de los libros no existe"}), 404
        
        if libro_ofrecido.get("estado_del_libro") != 'pausa':
            return jsonify({
                "error": f"El libro ofrecido debe estar en 'pausa'. Estado actual: {libro_ofrecido.get('estado_del_libro')}"
            }), 400

        # REALIZAR EL INTERCAMBIO:
        
        cursor.execute(
            "UPDATE libros SET usuario_id = %s, estado_del_libro = 'intercambiado' WHERE id = %s", 
            (id_usuario_ofrecido, id_libro_solicitado)
        )

        cursor.execute(
            "UPDATE libros SET usuario_id = %s, estado_del_libro = 'intercambiado' WHERE id = %s", 
            (id_usuario_solicitado, id_libro_ofrecido)
        )

        cursor.execute(
            "UPDATE intercambio_libro SET estado_del_intercambio = %s, fecha_final = NOW() WHERE codigo_intercambio = %s",
            ('completado', codigo)
        )

        conn.commit()
        
        return jsonify({
            "message": "Intercambio completado exitosamente",
            "codigo_intercambio": codigo,
            "detalles": {
                "libro_solicitado_id": id_libro_solicitado,
                "libro_ofrecido_id": id_libro_ofrecido,
                "nuevo_propietario_libro_solicitado": id_usuario_ofrecido,
                "nuevo_propietario_libro_ofrecido": id_usuario_solicitado
            }
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Error al aceptar intercambio: {str(e)}"}), 500
        
    finally:
        cursor.close()
        conn.close()

"""
Cancela una solicitud de intercambio. Puede solicitarlo el solicitante o el propietario.
"""
@intercambio_libros_bp.route('/cancelar_intercambio', methods=['POST'])
def cancelar_intercambio():
    
    data = request.get_json()
    codigo = data.get('codigo_intercambio')
    id_libro_solicitado = intercambio["id_libro_solicitado"]
    id_libro_ofrecido = intercambio["id_libro_ofrecido"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM intercambio_libro WHERE codigo_intercambio = %s", (codigo,))
        intercambio = cursor.fetchone()
        
        if not intercambio:
            return jsonify({"error": "Intercambio no encontrado"}), 404


        if intercambio.get("estado_del_intercambio") != 'espera':
            return jsonify({"error": "Solo los intercambios en 'espera' pueden cancelarse"}), 400

        cursor.execute("UPDATE libros SET estado_del_libro = %s WHERE id = %s", ('disponible', id_libro_ofrecido))
        cursor.execute("UPDATE libros SET estado_del_libro = %s WHERE id = %s", ('disponible', id_libro_solicitado))

        cursor.execute(
            "UPDATE intercambio_libro SET estado_del_intercambio = %s, fecha_final = NOW() WHERE codigo_intercambio = %s",
            ('cancelado', codigo)
        )

        conn.commit()
        return jsonify({"message": "Intercambio cancelado", "codigo_intercambio": codigo}), 200
    except Exception as e:

        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:

        cursor.close()
        conn.close()