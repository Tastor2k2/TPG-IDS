from flask import Blueprint,render_template,request

contacto_bp = Blueprint("contacto_bp", __name__)

@contacto_bp.route('/',methods=['GET','POST'])
def contacto():
    title="¡Contactate con Nosotros!"
    diccionario_horarios = {
        "Lunes":"08:30 - 22:00",
        "Martes":"08:30 - 22:00",
        "Miercoles":"08:30 - 22:00",
        "Jueves":"08:30 - 22:00",
        "Viernes":"08:30 - 22:00",
        "Sábado":"Cerrado",
        "Domingo":"Cerrado"
    }
    if request.method == 'POST':
        nombre = request.form.get('nombre_usuario')
        apellido = request.form.get('apellido_usuario')
        mail = request.form.get('email_usuario')
        telefono = request.form.get('telefono_usuario')
        mensaje = request.form.get('mensaje_usuario')
        return render_template('formulario_enviado.html',
                                titulo="Formulario Enviado Correctamente",
                                name=nombre,
                                surname=apellido,
                                email=mail,
                                tel=telefono,
                                mensj=mensaje)
    return render_template('contacto.html',titulo=title,horarios=diccionario_horarios)
