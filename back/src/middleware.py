#este archivo esta para verificar si hay en general sesion iniciada, tood esto para teener rutas privadas a las que solo usuarios con sesion iniciada pueden acceder
from flask import session, jsonify
from functools import wraps #functools es un modulo que viene con python y wraps una funcion que permite construir decoradores sin romper la info de la funcion general

#esto sirve para chequear si hay sesion iniciada o no, despues hay que pasarlo a las rutas que quiero que sea necesario el logeo
def loggin_obligatorio(f):
    @wraps(f)
    def decorador(*args, **kwargs): #args almacena la cantidad de parametros que va a recibir sin saber cuantos, mientras que kwargs almacena los tipo de parametros por nombre sin saber cuantos
        if "user_id" not in session:
            return jsonify({"error": "El usuario no esta loggeado"}), 401
        return f(*args, **kwargs)
    return decorador