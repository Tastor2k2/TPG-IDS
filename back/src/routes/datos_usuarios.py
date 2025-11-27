from flask import Blueprint, jsonify, request
from db import get_connection

datos_usuarios_bp  = Blueprint("datos_usuarios", __name__)

"""
Obtiene los datos del formulario de registro, compara con los datos existentes en la base para ver si alguno se repite,
y si se cumplen las condiciones registra al usuario en la base de datos.
"""
@datos_usuarios_bp.route('/registrar', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    nombre_usuario = data.get('nombre')
    email_usuario = data.get('email')
    contraseña_usuario = data.get('contraseña')
    telefono_usuario = data.get('telefono_usuario')
    direccion_usuario = data.get('direccion_usuario')
    dni_usuario = data.get('dni_usuario')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)   

    if not nombre_usuario or not email_usuario or not contraseña_usuario or not telefono_usuario or not direccion_usuario or not dni_usuario:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    cursor.execute("SELECT * FROM datos_usuario WHERE email_usuario = %s ", (email_usuario,))
    existe_mail = cursor.fetchone()

    if existe_mail:
        cursor.close()
        conn.close()
        return jsonify({"error": "EL EMAIL YA EXISTE"}), 400
    
    cursor.execute("SELECT * FROM datos_usuario WHERE nombre_usuario = %s", (nombre_usuario,))
    existe_nombre = cursor.fetchone()

    if existe_nombre:
         cursor.close()
         conn.close()
         return jsonify({"error": "EL NOMBRE DE USUARIO YA EXISTE"}), 400
    
    cursor.execute ("SELECT * FROM datos_usuario WHERE dni_usuario = %s", (dni_usuario,))
    existe_dni = cursor.fetchone()

    if existe_dni:
        cursor.close()
        conn.close()
        return jsonify({"error": "EL DNI YA EXISTE"}), 400
    
    cursor.execute ("SELECT * FROM datos_usuario WHERE telefono_usuario = %s", (telefono_usuario,))
    existe_telefono = cursor.fetchone()

    if existe_telefono:
        cursor.close()
        conn.close()
        return jsonify({"error": "EL NUMERO DE TELEFONO YA EXISTE"})

    cursor.execute("""
        INSERT INTO datos_usuario (nombre_usuario, email_usuario, contraseña_usuario, telefono_usuario, direccion_usuario, dni_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre_usuario, email_usuario, contraseña_usuario, telefono_usuario, direccion_usuario, dni_usuario))

    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "Usuario registrado con éxito"}, 201

"""
Comprueba que el mail o nombre de usuario y la contraseña ingresados en el formulario de inicio de sesion coincidan con los datos en la base,
y si se cumple lo pedido, se inicia la sesión del usuario.
"""
@datos_usuarios_bp.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    email_nombre_usuario = data.get('email_nombre_usuario')
    contraseña_usuario = data.get('contraseña')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if not email_nombre_usuario or not contraseña_usuario:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    cursor.execute("SELECT * FROM datos_usuario WHERE (email_usuario = %s OR nombre_usuario = %s) AND contraseña_usuario = %s", (email_nombre_usuario, email_nombre_usuario, contraseña_usuario,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return jsonify({
            "mensaje": "Login exitoso",
            "usuario": {
                "id": usuario["id"],
                "nombre": usuario["nombre_usuario"],
                "email": usuario["email_usuario"]
            }
        }), 200
    else:
        return jsonify({"error": "EMAIL O CONTRASEÑA INCORRECTOS"}), 401

    