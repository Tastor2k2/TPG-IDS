from flask import Blueprint,render_template

index_bp = Blueprint("index_bp",__name__)

@index_bp.route('/')
def index():
    """
    Propósito:
        - Mostrar la página principal del sitio.

        Comportamiento:
        - Define el título y renderiza 'index.html' pasando 'titulo'.

        Retorna:
        - Muestra la home.
    """
    title = "LibroXLibro"
    return render_template("index.html",titulo=title)
