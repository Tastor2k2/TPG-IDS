#!/bin/bash

# TODOS LOS CHEQUEOS DE INSTALACION SE OCULTAN DE LA SALIDA DE LA TERMINAL, PARA QUE NO MUEVA LOS MENSAJES DE CONFIRMACION.

# Ejecutar Para eliminar todo lo relacionado al backend:
# source eliminacion_backend.sh

eliminarCache() {
    cd src
    if [[ -d "__pycache__" ]]; then
        echo ""
        echo "---------------------------Eliminando __pycache__---------------------------"
        echo ""
        rm -rf __pycache__
    else
        echo ""
        echo "---------------------------No existe __pycache__---------------------------"
        echo ""
    fi
    cd ..
}

desactivarEntorno() {
    cd src
    if [[ -z "$VIRTUAL_ENV" ]]; then # True si da cero, queriendo decir que no hay entorno virtual activo.
        echo ""
        echo "---------------------------No hay entorno activo---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Desactivando el entorno---------------------------"
        echo ""
        deactivate
    fi
    cd ..
}

desinstalarFlaskMail() {
    if pip list | grep Flask-Mail > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Desinstalando Flask-Mail---------------------------"
        echo ""
        pip uninstall -y flask-mail
    else
        echo ""
        echo "---------------------------Flask-Mail no estaba instalado---------------------------"
        echo ""
    fi
}

desinstalarFlask() {
    if pip list | grep Flask > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Desinstalando Flask---------------------------"
        echo ""
        pip uninstall -y flask
    else
        echo ""
        echo "---------------------------Flask no estaba instalado---------------------------"
        echo ""
    fi
}

desinstalarPythonDotenv() {
    if pip list | grep python-dotenv > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Desinstalando python-dotenv---------------------------"
        echo ""
        pip uninstall -y python-dotenv
    else
        echo ""
        echo "---------------------------Python-dotenv no estaba instalado---------------------------"
        echo ""
    fi
}

desinstalarFlaskCors() {
    if pip list | grep Flask-Cors > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Desinstalando Flask-Cors---------------------------"
        echo ""
        pip uninstall -y flask-cors
    else
        echo ""
        echo "---------------------------Flask-Cors no estaba instalado---------------------------"
        echo ""
    fi
}

desinstalarMysqlConnector() {
    if pip list | grep mysql > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Desinstalando Mysql-Connector---------------------------"
        echo ""
        pip uninstall -y mysql-connector-python
    else
        echo ""
        echo "---------------------------Mysql-Connector no estaba instalado---------------------------"
        echo ""
    fi
}

eliminarEnv() {
    if [[ -f ".env" ]]; then
        echo ""
        echo "---------------------------Eliminando .env---------------------------"
        echo ""
        rm -rf .env
    else
        echo ""
        echo "---------------------------Archivo .env no estaba creado---------------------------"
        echo ""
    fi
}

eliminarVenv() {
    cd src
    if [[ -d ".venv" ]]; then
        echo ""
        echo "---------------------------Eliminando .venv---------------------------"
        echo ""
        rm -rf .venv
    else
        echo ""
        echo "---------------------------Carpeta .venv no estaba creada---------------------------"
        echo ""
    fi
    cd ..
}

eliminarCarpetas() {
    rm -r src
}

desinstalarPythonDotenv

desinstalarMysqlConnector

desinstalarFlaskCors

desinstalarFlaskMail

desinstalarFlask

desactivarEntorno

eliminarEnv

eliminarVenv

eliminarCache

eliminarCarpetas

