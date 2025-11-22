# 🎩 Scripts de bash del back end 🎩

Se desarrollaron 3 scripts encargados de manejar la creacion, activación y eliminacion de las carpetas requeridas para el entorno virtual del lado del back.
Son scripts muy similares a los del front, lo único que cambia son las dependencias que se terminan instalando.

## 📦 manager_backend.sh 📦

Este script es el principal de los 3 el cual permite crear el directorio con sus archivos y carpetas básicos para empezar a trabajar. Además el script recibe 1 solo parámetro el cual determina qué hacer por sobre las carpetas que viven en el directorio `back`, siendo posible realizar 2 acciones: __Activar y Eliminar__.

## 🔧 activacion_backend.sh 🔧

Este script se ejecuta desde el principal pasandole el parámetro `-a` de esta forma:

```shell
source manager_backend.sh -a
```

Este script se encarga de verificar que esté todo creado e instalado, para despues activar el entorno virtual con:

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

- Instala `flask-cors`

- Instala `flask_session`

- Instala `mysql-connector-python`

- Instala `python-dotenv`

- Instala `Werkzeuf`

## ⚠️ eliminacion_backend.sh ⚠️

Este script se ejecuta desde el principal pasandole el parámetro `-d` de esta forma:

```shell
source manager_backend.sh -d
```

Este script elimina lo que crea e instala __activacion_backend.sh__, realizando exacatemnte los pasos inversos a como hace las cosas el script encargado
de activar el entorno hasta la eliminacioń de la carpeta `.venv`. Adicionalmente este script __borra todas las carpetas dentro de back dejando solalemnte los 3 scripts y este archivo.md__

### Detalles extra

Los 2 scripts adicionales al principal, pueden ser ejecutados manualmente sin pasar por el manager, y causarán el mismo efecto documentado anteriormente.

Todos los scripts de bash de querer ser ejecutados, requieren que el usuario esté ubicado en este caso la carpeta __back__.