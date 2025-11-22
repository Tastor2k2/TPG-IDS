# 🎩 Scripts de bash del front end 🎩

Se desarrollaron 3 scripts encargados de manejar la creacion, activación y eliminacion de las carpetas requeridas para el entorno virtual del lado del front.

## 📦 manager_directorio_entorno_flask.sh 📦

Este script es el principal de los 3 el cual permite crear el directorio con sus archivos y carpetas básicos para empezar a trabajar. Además el script recibe 1 solo parámetro el cual determina qué hacer por sobre las carpetas que viven en el directorio del front-end, siendo posible realizar 2 acciones: __Activar y Eliminar__.

## 🔧 activacion_entorno_flask.sh 🔧

Este script se ejecuta desde el principal pasandole el parámetro `-a` de esta forma:

```shell
source manager_directorio_entorno_flask.sh -a
```

Este script se encarga de verificar que esté todo creado e instalado, para despues activar el entorno virtual con:

```shell
source .venv/bin/activate

```

Y luego lo ejecuta desde la carpeta `tpg` con:

```shell
python3 -m app_front_end.app
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

Este script se ejecuta desde el principal pasandole el parámetro `-d` de esta forma:

```shell
source manager_directorio_entorno_flask.sh -d
```

Este script elimina lo que crea e instala __activacion_entorno_flask.sh__, realizando exacatemnte los pasos inversos a como hace las cosas el script encargado
de activar el entorno hasta la eliminacioń de la carpeta `.venv`. Adicionalmente este script __borra todas las carpetas dentro de app_front_end dejando solalemnte los 3 scripts y este archivo.md__

### Detalles extra

Los 2 scripts adicionales al principal, pueden ser ejecutados manualmente sin pasar por el manager, y causarán el mismo efecto documentado anteriormente.

Todos los scripts de bash de querer ser ejecutados, requieren que el usuario esté ubicado en este caso la carpeta __app_front_end__.