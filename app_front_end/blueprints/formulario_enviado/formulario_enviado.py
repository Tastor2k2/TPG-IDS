from flask import Blueprint, render_template, request

formulario_enviado_bp = Blueprint("formulario_enviado_bp", __name__)

@formulario_enviado_bp.route("/",methods=["POST"])
def formulario_enviado():
    title = "Gracias Por Tu Mensaje"
    nombre = request.form.get("nombre_usuario")
    apellido = request.form.get("apellido_usuario")
    email = request.form.get("email_usuario")
    telefono = request.form.get("telefono_usuario")
    mensaje = request.form.get("mensaje_usuario")

    data = (nombre, apellido, email, telefono, mensaje)

    return render_template(
        "formulario_enviado.html",
        titulo=title,
        informacion_usuario=data
    )
