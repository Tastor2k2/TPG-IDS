from flask import Blueprint,render_template
funcionamiento_bp = Blueprint("funcionamiento_bp",__name__)

@funcionamiento_bp.route('/')
def funcionamiento():
    title="Funcionamiento"
    return render_template('funcionamiento.html',titulo=title)
