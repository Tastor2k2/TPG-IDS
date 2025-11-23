# Trabajo Práctico Grupal de Introducción al Desarrollo de Software - Curso Lanzillotta - 2C2025

<p align="center">
   <img src="app_front_end/static/images/logo_fondo_blanco.png" alt="TPG-IDS Libro x libro" width="600" height="600">
</p>

## Nombre del grupo

### git commit -m "."

## Nombre del proyecto

### Libro x Libro

## Integrantes

### Cancina, Matías Agustín - 111735

### Mochetti, Pérez Pedro - 114213

### Agliani, Ignacio - 114276

### Martinelli, Abril - 114515

### Ovejero, Lara - 112774

## Introducción

En este trabajo se realizó como proyecto una página web llamada Libro x Libro, la cual tiene como objetivo ser una herramienta intermediaria entre usuarios que desean intercambiar un libro por otro libro.
El intercambio se arregla entre ellos a través de la página y luego se concreta el intercambio de forma presencial.

## Resumen

Libro x LIbro es una página web dedicada a facilitar el intercambio de libros entre diferentes personas a través de una interfaz llamativa, fácil e intuitiva de usar, donde debe haber solicitudes y confirmaciones entre ellos para confirmar dichos intercambios en la página. Luego los usuarios podrán reunirse en persona para el intercambio de los libros que declararon en el intercambio con anterioridad. Cualquier persona que quiera registrarse y tenga libros para subir, podrá realizar todos los intercambios que desee, por ende el alcance de la página abarca mucho mas del ámbito académico apuntando a un público mas general.

## Decisiones de desarrollo

- Se tuvo como hipótesis principal que el proyecto se iba a encargar de facilitar el intercambio de libros entre usuarios que sean alumnos de la facultad de ingeniería de la universidad de buenos aires. Pero se optó por llevarlo a un público más general para no limitar su uso a libros académicos solamente, y que personas con todo tipo de libros puedan conseguir otros libros totalmente diferentes a los que poseen.

- Se evaluó tener una característica más para los libros, que indique si es favorito del usuario que lo subió, pero terminamos descartando esa idea puesto que no le vimos mucha utilidad ya que si un usuario busca un libro muy puntual, no le interesa mucho ver que libros favoritos poseen los demás usuarios y sentimos que iba a complejizar el desarrollo del proyecto.

- Se evaluó que a la hora de intercambiar los libros, se envien mails de confirmación a los usuarios los cuales tenían códigos que después se iban a ingresar en la página con un límite de tiempo para ir hasta la facultad a intercambiarlo y terminar de cerrar el mismo verificando los códigos. 
Pero finalmente no se desarrolló nada de eso puesto que sentimos que iba a demandar un desarrollo exhaustivo de confirmaciones a tiempo real por parte de ambos usuarios y resoluciones de casos borde como: por ejemplo:
¿Qué pasaría si se hace el intercambio en persona pero uno de los usuarios no confirmó en la página que se terminó el mismo? ¿Qué pasa si no se concretó el intercambio pero en la página ambos usuarios le dijeron erróneamente que  se concretó correctamente?
Entonces para evitar más complicaciones de diseño, tomamos un enfoque hacia un público más general donde puede haber diferentes puntos en común para intercambiar fijados por los usuarios en privado, se decidió dejar en la página misma las confirmaciones justas y necesarias para el correcto funcionamiento de la misma. Es decir, todo pasa a través de la página sin emails de por medio, y luego se arregla en privado cada usuario.

- Los usuarios pueden ver los datos de otros (telefono, direccion, dni, etc) solo cuando se solicita el intercambio, para que se puedan comunicar entre ellos. De no ofrecerse nada, ningun usuario puede ver los datos del otro, solo los libros.

## Solución propuesta

Se propuso como solución para el funcionamiento correcto de la página, que el usuario debe estar iniciado en la misma para utilizar su funcionalidad principal, la cual es intercambiar sus libros con otro usuario. Para ello se necesita que el usuario tenga como mínimo 1 libro subido a su perfil para intercambiar. Esas 2 condiciones se validan desde el lado del front, denegando al usuario la posibilidad de usar correctamente la página si alguna de ellas no se cumple.

A la hora de crear un usuario, se rqeuieren llenar obligatoriamente estos campos:

- Nombre de usuario

- Email

- Confirmación del Email

- Contraseña

- Teléfono

- Dirección

- DNI

Si uno de estos campos falta, se valida desde el front y se vuelve a pedir que ingrese el campo faltante con un dato válido para registrarse. Una vez registrado el usuario, debe iniciar sesión poniendo su mail (o nombre de usuario) y contraseña. Esto se valida desde la base de datos, enviandole el resultado de la solicitud al front y de ser necesario volver a introducir la contraseña o el mail, se le informará al usuario.

Para cargar un libro, el usuario debe estar iniciado en la página, ir a su propio perfil y hacer click en cargar libro. Se le piden los siguientes campos a llenar:

- Título

- Autor

- Editorial

- Código isbn

- Temática

- Imagen (png, jpg, jpeg)

El libro se guarda en la base de datos del usuario, y se validan previamente que se hayan completado los campos correctamente. Luego ese libro cargado ya queda en estado disponible para que otros usuarios puedan verlo y ofrecer otros libros como propuesta de intercambio.

Cuando un usuario tiene __como mínimo un libro cargado__ que desea intercambiar y está con la __sesión iniciada__, puede buscar un libro en particular que esté disponible a través de la barra de búsqueda mediante el código isbn, el nombre, temática, autor, y por todos los campos de cada libro en la base de datos. Cuando se encuentra un libro de interés, el usuario envía una petición al usuario solicitado ofreciéndole un libro a cambio de otro de su biblioteca.
Una vez hecho eso, el libro ofrecido pasa a estar en estado de `pausa`, y deja de ser visible para los demás usuarios que quieran buscarlo para intercambiar (esto se logra en el back y se valida que no vuelvan a aparecer para buscar en la barra de búsqueda desde el front). Luego queda creada la solicitud del intercambio con el estado `espera`, con el libro ofrecido por el usuario solicitante en `pausa` y con el libro solicitado aún en `disponible` ya que puede seguir recibiendo propuestas de intercambio por ese libro y luego decidir cual aceptar.

Mientras se espera respuesta del usuario solicitado, el usuario solicitante puede cancelar el intercambio por si se arrepiente o si el usuario solicitado no respondió nunca la petición. 
De no querer cancelar la solicitud, queda en manos del usuario solicitado aceptar o nó.

Si se __cancela la solicitud__, el libro ofrecido por el usuario solicitante, pasa a estar `disponible` de nuevo, el intercambio queda en estado `cancelado` y se guarda en el historial de cada usuario el resultado del intercambio cancelado con la información de los libros, los datos del usuario que envió la solicitud y la fecha de finalización del intercambio.

El intercambio __sólo puede ser aceptado por el usuario solicitado__. De ser asi, se realiza el intercambio de los libros, cambiando los dueños de los mismos en la base de datos, luego ambos libros pasan a tener el estado de `intercambiado`, y el intercambio se guarda en el historial de los usuarios con el estado de `finalizado` también guardando los datos mencionados a la hora de cancelarlo.

El intercambio figura en la página como `finalizado` pero luego cada usuario debe coordinar con el otro para elegir un punto en común y realizar dicho intercambio (por eso a cada usuario cuando se registra se le pide la direccion, telefono y dni).

Para volver a intercambiar, el usuario debe tener mínimo un libro en estado `disponible`, es decir, el libro que recibió como queda en estado `intercambiado` no puede volver a ofrecerse, a menos de que se vuelva a cargar a la página. __Siempre que se carga un libro aparece disponible.__

## Composición del front-end y back-end

### Front

...

#### [scripts](app_front_end/SCRIPTS_FRONT.md)

### Back

#### Tarea

El back se encarga del manejo de la base de datos, recibir solicitudes del front y responderlas enviando resultados en formato JSON y realizar verificaciónes de validación de acceso y cambios a la base de datos.

#### Tablas

Se disponen de 3 tablas para el correcto manejo de la base de datos, las cuales son: `datos_usuario`, `libros` y `intercambio_libro`.

#### Composición de archivos

Se compone de una carpeta `src` donde se encuentra la base de datos (`init_db.sql`), el inicializador de la base (`init_db.py`), el archivo que genera la conexión de la base de datos con los archivos.py (`db.py`), el archivo principal encargado de conectar las direcciones mediante blueprints (`app.py`), una carpeta de imagenes para los libros (`static/images`) y la carpeta `routes` donde se alojan las direcciones con los diferentes endpoints que resuelven las consultas del front.

Dentro de `routes` se encuentran todos los blueprints referenciados por `app.py` y sus endpoints correspondientes.

#### Explicación y ejemplos de uso de cada archivo y endpoint

- __carga_libros.py:__ Maneja la carga de todos los datos de los libros (menos la imagen) a la base de datos de cada usuario.
    - __carga_libro()__ Carga un libro en la base de datos en la tabla de libros, referenciando al usuario que lo cargó.
    - __obtener_libros(usuario_id)__ Obtiene todos los libros de un usuario específico y los retorna en orden descendente segun su fecha de carga a la pagina.
    - __eliminar_libro(libro_id)__ Elimina un libro de la base de datos (solo si está en estado 'disponible'). `(capaz no se usa)`

- __carga_libros_imagenes.py__ Maneja la subida de imagenes asociadas a los libros cargados mediante el archivo mencionado anteriormente.
    - __allowed_file(filename)__ Valida si la extensión de la imagen es válida (`png, jpg ó jpeg`).
    - __subir_imagen(libro_id)__ Llama a `allowed_file` para validar la imagen y de ser válida, la guarda en `static/images` del back y carga la ruta en la base de datos.

- __datos_usuarios.py__ Maneja el registro y el inicio de sesión de cada usuario.
    - __registrar_usuario()__ Guarda los datos de registro del usuario en la base de datos verificando que no se repitan campos como el mail, el nombre de usuario, etc.
    - __login_usuario()__ Verifica que el mail y contraseña del usuario existan en la base de datos, luego envia al front las respuestas a las consultas a la base de datos.

- __intercambio_libros.py__ Maneja la lógica y validaciones necesarias para el correcto funcionamiento del intercambio de libros entre usuarios.
    - __tiene_libros(usuario_id)__ Muestra la cantidad total de libros que tiene el usuario.
    - __solicitar_intercambio()__ Crea la solicitud de intercambio de un usuario solicitante hacia un usuario solicitado, validando que los campos a completar sean correctos.
    - __aceptar_intercambio()__ Maneja la lógica del intercambio aceptado por el usuario solicitado, validando los campos necesarios y luego cambiando los libros de un usuario hacia el otro,
    guardando esa información en la base de datos de cada usuario y finalmente cambiando el estado del intercambio a `completado` y el estado de los libros a `intercambiado`.
    - __cancelar_intercambio()__ Cancela una solicitud de intercambio. Puede solicitarlo el solicitante o el propietario.
    - __mostrar_intercambio(usuario_id)__ Le envia al front las consultas a la base de datos necesarias para hacer un seguimiento de los intercambios según su estado, recolectando información de los usuarios y libros involucrados.

- __listar_libros.py__ Maneja la lógica del muestreo de libros para la biblioteca y la barra de búsqueda.
    - __listar_libros()__ Devuelve todos los libros disponibles para intercambio (de todos los usuarios) excluyendo los libros del propio usuario solicitante.
    - __buscar_libros()__ Busca el libro en la base de datos (mediante cualquier campo del libro presente en la tabla) y permite que se puedan poner palabras similares a la buscada.

#### [scripts](back/SCRIPTS_BACK.md)

## Tecnología usada

- Lenguajes de programación: Python 3.12.3, Javascript 2015 (ES6) y bash.

- Lenguaje de marcado: HTML

- Lenguaje de hoja de estilos: CSS

- Framework: Flask

- Base de datos: MYSQL

- Dependencias varias: Flask Mail, Flask Cors, Flask Session, Dotenv, Mysql Connector, Request y Werkzeug

### Casos de uso de dependencias

- __Flask mail:__ Se utiliza para el template `contacto.html` donde se envían consultas hacia la página, suferencias, y demás mensajes. `(falta implementar esa parte)`
- __Flask Cors:__ ?? quizas quitarlo
- __Flask Session:__ Se utiliza para las validaciones de sesion iniciada de usuarios, para utilizar las funcionalidades principales de la página.
- __Dotenv:__ Se utiliza para el manejo de archivos .env.
- __Mysql Connector:__ Se utiliza para la comunicación entre la base de datos y el front.
- __Request:__ Se utiliza para la obtención de los campos de los formularios del front.
- __Werkzeug:__ Convierte un nombre inapropiado en algo seguro para guardarlo en la base de datos (evitar imagenes con nombres demasiado largos).

## Conclusión

...



