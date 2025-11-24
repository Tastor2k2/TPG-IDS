from flask import Blueprint, render_template, session, redirect, url_for, current_app, request,jsonify
import requests

intercambio_bp = Blueprint("intercambio_bp", __name__)

@intercambio_bp.route('/', methods=["GET", "POST"])
def intercambio():
    """
    Propósito:
      - Permitir que un usuario autenticado solicite un intercambio entre un libro ajeno
        (libro_solicitado) y uno propio (libro_ofrecido).

    Flujo (GET):
      - Requiere sesión: si no existe session["user_id"], redirige a iniciar sesión.
      - Toma 'libro_solicitado'. Si falta, 400.
      - Pide al backend los libros del usuario: GET {BACK_URL}/libros/mis-libros/<id_usuario>.
      - Si no hay libros en "disponible", redirige a cargar libro.
      - Pide la biblioteca filtrada: GET {BACK_URL}/libros/libros?usuario_id=<id_usuario>.
      - Renderiza 'intercambio.html' con: libros_usuario, biblioteca y libro_solicitado.

    Flujo (POST):
      - Lee 'libro_ofrecido' del formulario y 'libro_solicitado' de la query; si falta el solicitado, 400.
      - Obtiene el detalle del libro solicitado: GET {BACK_URL}/libros/libros/<libro_solicitado>.
        Si no existe, 404. Toma 'usuario_id' del JSON (dueño del libro solicitado).
      - Arma el payload (data que viaja adentro de una response):
          {
            "id_libro_solicitado": <int>,
            "id_libro_ofrecido": <int>,
            "id_usuario_ofrecido": <id_usuario_en_sesion>,
            "id_usuario_solicitado": <dueño_libro_solicitado>
          }
      - Crea la solicitud de intercambio: POST {BACK_URL}/libros/solicitar_intercambio (JSON).
      - Redirige al perfil del usuario: url_for("perfil_bp.perfil", id_usuario=session["user_id"]).

    Dependencias:
      - 'app.config["BACK_URL"]' configurado.
      - Sesión con 'session["user_id"]'.
      - Template 'intercambio.html'.
      - Endpoints del backend mencionados arriba que devuelvan JSON adecuado.

    Retornos:
      - GET 200: muestra formulario de intercambio.
      - POST 302 (encontrado): redirección al perfil si la creación fue enviada.
      - 400/404: string de error según validaciones básicas.
    """
    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    BACK_URL = current_app.config["BACK_URL"]
    id_usuario = session["user_id"]

    if request.method == "GET":
        libro_solicitado = request.args.get("libro_solicitado", type=int)
        if not libro_solicitado:
            return jsonify({"Error":"Error: no seleccionaste ningún libro"}), 400

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
        return jsonify({"Error": "falta libro solicitado"}), 400

    r_libro = requests.get(f"{BACK_URL}/libros/libros/{libro_solicitado}")
    if r_libro.status_code != 200:
        return jsonify({"Error": "no se encontró el libro solicitado"}), 404

    usuario_solicitado = r_libro.json().get("usuario_id")

    data = {
        "id_libro_solicitado": libro_solicitado,
        "id_libro_ofrecido": libro_ofrecido,
        "id_usuario_ofrecido": id_usuario,
        "id_usuario_solicitado": usuario_solicitado
    }

    requests.post(f"{BACK_URL}/libros/solicitar_intercambio", json=data)

    return redirect(url_for("perfil_bp.perfil", id_usuario=id_usuario))
