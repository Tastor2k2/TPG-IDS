from flask import Blueprint, session, redirect, url_for

logout_bp = Blueprint("logout_bp", __name__)

@logout_bp.route("/cerrar_sesion")
def cerrar_sesion():
    """
    Cierra la sesión del usuario.

    - Propósito: eliminar todos los datos de la sesión actual (logout).
    - Flujo: 'session.clear()' borra las claves de sesión (p. ej. user_id).
    - Retorno: redirige a la página de inicio (index_bp.index).
    """
    session.clear()
    return redirect(url_for("index_bp.index"))
