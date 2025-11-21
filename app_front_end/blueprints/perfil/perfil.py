from flask import Blueprint,Flask,render_template,request

perfil_bp = Blueprint("perfil_bp",__name__)

@perfil_bp.route('/')
def perfil():
    title="Mi Perfil"
    return render_template('perfil.html',titulo=title)
