from flask import Blueprint, render_template

formulario_enviado_bp = Blueprint("formulario_enviado_bp", __name__)

@formulario_enviado_bp.route("/",methods=["GET"])
def formulario_enviado():
    """
    Propósito:
        - Mostrar la página “Formulario Enviado”.

    Comportamiento:
        - Define el título y renderiza el template 'formulario_enviado.html'
        pasando la variable 'titulo'.

    Dependencias:
        - Template 'formulario_enviado.html'.

    Retorno:
        - Muestra la página.    
    """
    title = "Gracias Por Tu Mensaje"

    return render_template(
        "formulario_enviado.html",
        titulo=title,
    )
