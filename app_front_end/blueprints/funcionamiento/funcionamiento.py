from flask import Blueprint,render_template
funcionamiento_bp = Blueprint("funcionamiento_bp",__name__)

@funcionamiento_bp.route('/')
def funcionamiento():
    """
    Propósito:
      - Mostrar la página informativa con cómo funciona el servicio.

    Comportamiento:
      - Define el título de la página y renderiza el template 'funcionamiento.html'
        pasando la variable 'titulo'.

    Requisitos:
      - Template 'templates/funcionamiento.html' disponible.

    Retorna:
      - La página de funcionamiento.

    """
    title="Funcionamiento"
    return render_template('funcionamiento.html',titulo=title)
