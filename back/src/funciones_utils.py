from flask import session, jsonify

def validar_sesion():
    if "user_id" not in session:
        return jsonify({"msg": "Tenes que iniciar sesion"}), 401
    return None