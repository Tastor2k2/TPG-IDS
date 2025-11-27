# 🎩 Scripts de bash del back end 🎩

Se desarrollaron 2 scripts encargados de manejar la creacion, activación y eliminacion de los requerimientos para hacer funcionar el entorno virtual del lado del back.
Son scripts muy similares a los del front, lo único que cambia son las dependencias que se terminan instalando.

## 🔧 activacion_backend.sh 🔧

Este script se ejecuta de esta forma:

```shell
source activacion_backend.sh
```

Luego se encarga de verificar que esté todo creado e instalado, para despues activar el entorno virtual con:

```shell
source .venv/bin/activate
```

Si no hay nada preparado para activar el entorno, se realizan estos pasos en el siguiente orden, de arriba hacia abajo:

- Crea el archivo `.env`

- Accede al directorio `src`

- Instala `python3.12`

- Instala `pip3`

- Instala `python3.12-venv`

- Crea la carpeta `.venv`

- Activa el entorno virtual

- Instala `flask`

- Instala `Flask-Mail`

- Instala `flask_session`

- Instala `mysql-connector-python`

- Instala `python-dotenv`

- Instala `Werkzeuf`

Despues de tener todas las dependencias y el entorno activado, se inicializa la base de datos con el siguiente comando dentro de la carpeta `src`:

```shell
python3 init_db.py
```

Finalmente se ejecuta `app.py` dentro de la carpeta `src` con esta linea:

```shell
python3 app.py
```

## ⚠️ eliminacion_backend.sh ⚠️

Este script se ejecuta de esta forma:

```shell
source eliminacion_backend.sh
```

Este script elimina lo que crea e instala __activacion_backend.sh__, realizando exacatemnte los pasos inversos a como hace las cosas el script encargado
de activar el entorno hasta la eliminacioń de la carpeta `.venv`.

### Detalles extra

Todos los scripts de bash del backend, de querer ser ejecutados, requieren que el usuario esté ubicado en este caso la carpeta __back__.

Se asume que las carpetas del proyecto necesarias para hacerlo funcionar ya existen.
