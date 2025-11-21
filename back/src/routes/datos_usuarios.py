from flask import Blueprint, jsonify, request
from db import get_connection

datos_usuarios_bp  = Blueprint("datos_usuarios", __name__)

#cargamos lo resibido en el formulario a la tabla datos_usuario
@datos_usuarios_bp.route('/registrar', methods=['POST']) #nose como esta puesto en el front el form, sino habria que cambiar registrar y el metodo
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

    #chequeamos si el usuario completo todos los campos:
    if not nombre_usuario or not email_usuario or not contraseña_usuario or not telefono_usuario or not direccion_usuario or not dni_usuario:
        return jsonify({"error": "Faltan campos obligatorios"}), 400


    #chequeamos si existe el mail:
    cursor.execute("SELECT * FROM datos_usuario WHERE email_usuario = %s ", (email_usuario,))
    existe_mail = cursor.fetchone()

    #si existe el mail:
    if existe_mail:
        cursor.close()
        conn.close()
        return jsonify({"error": "EL EMAIL YA EXISTE"}), 400
    
    #chequeamos si existe el nombre de usuario:
    cursor.execute("SELECT * FROM datos_usuario WHERE nombre_usuario = %s", (nombre_usuario,))
    existe_nombre = cursor.fetchone()

    #si existe el nombre de usuario:
    if existe_nombre:
         cursor.close()
         conn.close()
         return jsonify({"error": "EL NOMBRE DE USUARIO YA EXISTE"}), 400
    
    #chequeamos si el dni existe:
    cursor.execute ("SELECT * FROM datos_usuario WHERE dni_usuario = %s", (dni_usuario,))
    existe_dni = cursor.fetchone()

    #si existe el dni:
    if existe_dni:
        cursor.close()
        conn.close()
        return jsonify({"error": "EL DNI YA EXISTE"}), 400
    
    
    #chequeamos si el telefono existe:
    cursor.execute ("SELECT * FROM datos_usuario WHERE telefono_usuario = %s", (telefono_usuario,))
    existe_telefono = cursor.fetchone()

    #si existe:
    if existe_telefono:
        cursor.close()
        conn.close()
        return jsonify({"error": "EL NUMERO DE TELEFONO YA EXISTE"})

    #si no existe ni el nombre ni el mail ni el dni ni el numero de telefono y completo todos los campos:
    cursor.execute("""
        INSERT INTO datos_usuario (nombre_usuario, email_usuario, contraseña_usuario, telefono_usuario, direccion_usuario, dni_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre_usuario, email_usuario, contraseña_usuario, telefono_usuario, direccion_usuario, dni_usuario))

    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "Usuario registrado con éxito"}, 201


@datos_usuarios_bp.route('/login', methods=['POST']) #nose como esta puesto en el front el form, sino habria que cambiar login y el metodo
def login_usuario():
    data = request.get_json()
    email_nombre_usuario = data.get('email_nombre_usuario')
    contraseña_usuario = data.get('contraseña')


    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    #chequeamos si el usuario completo todos los campos:
    if not email_nombre_usuario or not contraseña_usuario:
        return jsonify({"error": "Faltan campos obligatorios"}), 400


    #chequeamos si existe el usuario:
    cursor.execute("SELECT * FROM datos_usuario WHERE (email_usuario = %s OR nombre_usuario = %s) AND contraseña_usuario = %s", (email_nombre_usuario, email_nombre_usuario, contraseña_usuario,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    #si el usuario existe:
    if usuario:
        #guardamos sesion:
        "user_id"=usuario["id"]
        "nombre"=usuario["nombre_usuario"]
        "email"=usuario["email_usuario"]
        return jsonify({
            "mensaje": "Login exitoso",
            "usuario": {"nombre": usuario["nombre_usuario"],"email": usuario["email_usuario"], "user_id": usuario["id"]}}), 200
    else:
        return jsonify({"error": "EMAIL O CONTRASEÑA INCORRECTOS"}), 401

    