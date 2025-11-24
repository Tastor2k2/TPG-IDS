from flask import Blueprint, render_template, session, redirect, url_for, current_app, request
import requests

intercambio_bp = Blueprint("intercambio_bp", __name__)

@intercambio_bp.route('/', methods=["GET", "POST"])
def intercambio():

    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    BACK_URL = current_app.config["BACK_URL"]
    id_usuario = session["user_id"]

    if request.method == "GET":
        libro_solicitado = request.args.get("libro_solicitado", type=int)
        if not libro_solicitado:
            return "Error: no seleccionaste ningún libro", 400

        r = requests.get(f"{BACK_URL}/libros/mis-libros/{id_usuario}")
        mis_libros = r.json().get("libros", [])
        libros_disponibles = [libro for libro in mis_libros if libro.get("estado_del_libro") == "disponible"]
        if len(libros_disponibles) == 0:
            return redirect(url_for("cargar_libro_bp.cargar_libro"))

        r_biblio = requests.get(
            f"{BACK_URL}/libros/libros",
            params={"usuario_id": id_usuario}
        )
        biblioteca = r_biblio.json().get("libros", [])

        return render_template(
            "intercambio.html",
            libros_usuario=mis_libros,
            biblioteca=biblioteca,
            libro_solicitado=libro_solicitado
        )

    libro_ofrecido = request.form.get("libro_ofrecido", type=int)

    libro_solicitado = request.args.get("libro_solicitado", type=int)
    if not libro_solicitado:
        return "Error: falta libro solicitado", 400

    r_libro = requests.get(f"{BACK_URL}/libros/libros/{libro_solicitado}")
    if r_libro.status_code != 200:
        return "Error: no se encontró el libro solicitado", 404

    usuario_solicitado = r_libro.json().get("usuario_id")

    data = {
        "id_libro_solicitado": libro_solicitado,
        "id_libro_ofrecido": libro_ofrecido,
        "id_usuario_ofrecido": id_usuario,
        "id_usuario_solicitado": usuario_solicitado
    }

    requests.post(f"{BACK_URL}/libros/solicitar_intercambio", json=data)

    return redirect(url_for("perfil_bp.perfil", id_usuario=id_usuario))
