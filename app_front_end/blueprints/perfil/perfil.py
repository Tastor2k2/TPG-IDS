from flask import Blueprint, render_template, request, session, jsonify, current_app, redirect, url_for
import requests

perfil_bp = Blueprint("perfil_bp", __name__)

@perfil_bp.route("/usuario/<int:id_usuario>", methods=["GET", "POST"])
def perfil(id_usuario):
    """
    Propósito:
        - Mostrar el historial de intercambios del usuario autenticado.
        - Permitir acciones sobre intercambios (aceptar / cancelar).

    Flujo:
        Seguridad:
        - Requiere sesión: si no existe 'session["user_id"]', salta un error 401 (no autorizado).
        - Debe coincidir el id de la URL con 'session["user_id"]', si no, salta un 403 (accedo denegado).

        Si es GET (no realiza intercambios):
        1) Lee 'BACK_URL' de config y el id de la sesión.
        2) Pide al backend el historial:
            POST {BACK_URL}/libros/intercambios/historial/<id_usuario>
        3) Si la respuesta no es 200, el historial es vacío.
        4) Renderiza 'perfil.html' pasando:
            - nombre, email (desde sesión)
            - id (desde sesión)
            - historial (pendientes, completados, cancelados)
            - titulo

    POST:
        1) Lee 'accion' y 'codigo_intercambio' del form. Si faltan, salta un error 400.
        2) Dependiendo la accion seleccionada:
            - "aceptar": registra en la base de datos el intercambio y lo marca como 'completado'.
            - "cancelar": registra en la base de datos el intercambio y lo marca como 'cancelado'.
        3) Redirige al propio perfil para ver cambios:
            redirect(url_for("perfil_bp.perfil", id_usuario=session["user_id"]))

    Dependencias:
        - 'app.config["BACK_URL"]' configurado.
        - Endpoints del backend mencionados arriba que devuelvan JSON adecuado.
        - Template 'perfil.html'.

    Retornos:
        - Template del perfil con historial.
        - Si el intercambio sale bien, se redirecciona al perfil tras procesar acción.
        - Si hay errores, devuelve JSONs 401/403/400 según el caso.
    """
    title = "Mi perfil"
    # PROTECCIÓN
    if "user_id" not in session:
        return jsonify({"Error": "Debes iniciar sesión"}), 401

    if session["user_id"] != id_usuario:
        return jsonify({"Error": "Acceso no autorizado"}), 403

    BACK_URL = current_app.config["BACK_URL"]
    id_usuario = session["user_id"]

    if request.method == "POST":

        accion = request.form.get("accion")
        codigo = request.form.get("codigo_intercambio")

        if not accion or not codigo:
            return jsonify({"error": "Datos insuficientes"}), 400

        if accion == "aceptar":
            requests.post(
                f"{BACK_URL}/libros/aceptar_intercambio",
                json={"codigo_intercambio": codigo}
            )

        elif accion == "cancelar":
            requests.post(
                f"{BACK_URL}/libros/cancelar_intercambio",
                json={"codigo_intercambio": codigo}
            )

        # Volver al perfil para ver cambios
        return redirect(url_for("perfil_bp.perfil", id_usuario=id_usuario))

    respuesta_back = requests.get(
        f"{BACK_URL}/libros/intercambios/historial/{id_usuario}"
    )

    if respuesta_back.status_code != 200:
        historial = {"pendientes": [], "completados": [], "cancelados": []}
    else:
        historial = respuesta_back.json()

    return render_template(
        "perfil.html",
        nombre=session["nombre"],
        email=session["email"],
        id=id_usuario,
        historial=historial,
        titulo=title
    )
