from flask import Blueprint,render_template
sobre_nosotros_bp = Blueprint("sobre_nosotros_bp",__name__)

@sobre_nosotros_bp.route('/')
def sobre_nosotros():
    """
    Propósito:
        - Mostrar la página “Sobre Nosotros”.

    Comportamiento:
        - Define el título y renderiza el template 'sobre_nosotros.html'
        pasando la variable 'titulo'.

    Dependencias:
        - Template 'sobre_nosotros.html'.

    Retorno:
        - Muestra la página.    
    """
    title="¡Sobre Nosotros!"
    return render_template('sobre_nosotros.html',titulo=title)
