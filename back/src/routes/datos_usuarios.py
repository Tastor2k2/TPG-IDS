from flask import Blueprint, jsonify, request
from src.db import get_connection

datos_usuarios_bp  = Blueprint("datos", __name__)

#cargamos lo resibido en el formulario a la tabla datos_usuario
@datos_usuarios_bp.route('/registrar', methods=['POST']) #nose como esta puesto en el front el form, sino habria que cambiar registrar y el metodo
def registrar_usuario():
    data = request.get_json()
    nombre_usuario = data['nombre']
    email_usuario = data['email']
    contraseña_usuario = data['contraseña']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    #chequeamos si el usuario completo todos los campos:
    if not nombre_usuario or not email_usuario or not contraseña_usuario:
        return jsonify({"error": "Faltan campos obligatorios"}), 400


    #chequeamos si existe el usuario:
    cursor.execute("SELECT * FROM datos WHERE email_usuario = %s", (email_usuario,))
    existe = cursor.fetchone()

    #si existe:
    if existe:
        cursor.close()
        conn.close()
        return jsonify({"ERROR: EL USUARIO YA EXISTE"}), 400
    
    #si no existe y completo todos los campos:
    cursor.execute("""
        INSTERT INTO datos (nombre_usuario, email_usuario, contraseña_usuario)
        VALUES (%s, %s, %s)
    """), (nombre_usuario, email_usuario, contraseña_usuario)

    conn.commit()
    cursor.close()
    conn.close()
    

