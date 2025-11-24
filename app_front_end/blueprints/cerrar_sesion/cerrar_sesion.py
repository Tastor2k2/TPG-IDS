from flask import Blueprint, session, redirect, url_for

logout_bp = Blueprint("logout_bp", __name__)

@logout_bp.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()
    return redirect(url_for("index_bp.index"))
