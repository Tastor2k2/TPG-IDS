# 🎩 Scripts de bash del front end 🎩

Se desarrollaron 2 scripts encargados de manejar la creacion, activación y eliminacion de los requerimientos para hacer funcionar el entorno virtual del lado del front.

## 🔧 activacion_entorno_flask.sh 🔧

Este script se ejecuta de esta forma:

```shell
source activacion_entorno_flask.sh
```

Luego se encarga de verificar que esté todo creado e instalado, para despues activar el entorno virtual con:

```shell
source .venv/bin/activate

```

Y luego lo ejecuta desde la carpeta `app_front_end` con:

```shell
python3 app.py
```

Si no hay nada preparado para activar el entorno, se realizan estos pasos en el siguiente orden, de arriba hacia abajo:

- Instala `python3.12`

- Instala `pip3`

- Instala `python3.12-venv`

- Crea la carpeta `.venv`

- Crea el archivo `.env` (Para la utilización segura de los datos de usuario)

- Activa el entorno virtual

- Instala `flask`

- Instala `Flask-Mail`

- Instala `python-dotenv`

- Instala `mysql-connector-python`

- Instala `requests`

## ⚠️ eliminacion_entorno_flask.sh ⚠️

Este script se ejecuta de esta forma:

```shell
source eliminacion_entorno_flask.sh
```

Este script elimina lo que crea e instala __activacion_entorno_flask.sh__, realizando exacatemnte los pasos inversos a como hace las cosas el script encargado
de activar el entorno hasta la eliminacioń de la carpeta `.venv`.

### Detalles extra

Todos los scripts de bash del frontend, de querer ser ejecutados, requieren que el usuario esté ubicado en este caso la carpeta __app_front_end__.