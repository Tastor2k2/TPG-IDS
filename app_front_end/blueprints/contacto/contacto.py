from flask import Blueprint,render_template,request, current_app
from flask_mail import Message
import os

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
        email_usuario = request.form.get('email_usuario')
        telefono = request.form.get('telefono_usuario')
        mensaje = request.form.get('mensaje_usuario')

        mail_instance = current_app.extensions['mail']

        msg_admin = Message(
            subject=f"Nuevo mensaje de LibroxLibro de {nombre} {apellido}",
            recipients=["libroxlibro@gmail.com"],
            body=f"""
            Nueva consulta desde LibroxLibro:

            Nombre: {nombre} {apellido}
            Email: {email_usuario}
            Teléfono: {telefono}

            Mensaje:
            {mensaje}
            """
        )
        mail_instance.send(msg_admin)

        # Mail para el usuario
        msg_usuario = Message(
            subject="Recibimos tu mensaje - LibroxLibro",
            recipients=[email_usuario],
            body=f"""
            Hola {nombre},

            Gracias por contactarte con LibroxLibro.
            Recibimos tu mensaje y te responderemos a la brevedad.

            Tu mensaje:
            {mensaje}

            Saludos,
            El equipo de LibroxLibro
            """
            )
        mail_instance.send(msg_usuario)

        return render_template(
            'formulario_enviado.html',
            titulo="Formulario Enviado Correctamente",
            name=nombre,
            surname=apellido,
            email=email_usuario,
            tel=telefono,
            mensj=mensaje
        )

    return render_template(
        'contacto.html',
        titulo=title,
        horarios=diccionario_horarios
    )

