from flask import Blueprint,render_template,request, current_app
from flask_mail import Message
import traceback


contacto_bp = Blueprint("contacto_bp", __name__)

"""
Esta función envía al mail rellenado en el formularo,
un mail donde se le muestra que su mensaje de consulta
fué enviado exitosamente junto con sus datos ingresados.
Envía un mail a la direccion libroxlibrooficial@gmail.com
donde el emisor es el mail rellenado en el formulario y
recibe el mensaje insertado.
"""
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

        try:
            mail_instance = current_app.extensions['mail']
            # Mail para el administrador
            msg_admin = Message(
                subject=f"Nuevo mensaje de LibroxLibro de {nombre} {apellido}",
                recipients=["libroxlibrooficial@gmail.com"],
                body=f"""Nueva consulta desde LibroxLibro:
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
                body=f"""Hola {nombre},
Gracias por contactarte con LibroxLibro.
Recibimos tu mensaje y te responderemos a la brevedad.
Tu mensaje: {mensaje}
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
        
        except Exception as e:
            print(f"Error al enviar email: {str(e)}")
            traceback.print_exc()
            return render_template('500.html', error=str(e)), 500

    return render_template(
        'contacto.html',
        titulo=title,
        horarios=diccionario_horarios
    )
