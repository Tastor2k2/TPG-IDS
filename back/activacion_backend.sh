#!/bin/bash

# TODOS LOS CHEQUEOS DE INSTALACION SE OCULTAN DE LA SALIDA DE LA TERMINAL, PARA QUE NO MUEVA LOS MENSAJES DE CONFIRMACION.

# Ejecutar Para Crear y activar el backend:
# source activacion_backend.sh

instalarPython3() {
    if python3 --version > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Python3 ya esta instalado---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Instalando Python3---------------------------"
        echo ""
        sudo apt install python3
    fi
}

instalarPip3() {
    if pip3 --version > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Pip3 ya esta instalado---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Instalando Pip3---------------------------"
        echo ""
        sudo apt install python3-pip
    fi
}

instalarFlaskMail() {
    if pip list | grep Flask-Mail > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Flask-Mail ya está instalado---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Instalando Flask-Mail---------------------------"
        echo ""
        pip install Flask-Mail
    fi
}

crearVenv() {
    if [[ -d ".venv" ]]; then
        echo ""
        echo "---------------------------Carpeta .venv ya estaba creada---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Creando .venv---------------------------"
        echo ""
        python3 -m venv .venv
    fi
}

ActivacionEntornoVirtual() {
    if [[ -z "$VIRTUAL_ENV" ]]; then # True si da cero, queriendo decir que no hay entorno virtual activo.
        echo ""
        echo "---------------------------Se activará el entorno virtual---------------------------"
        echo ""
        source .venv/bin/activate
    else
        echo ""
        echo "----------------Entorno virtual activado previamente en: $VIRTUAL_ENV----------------"
        echo ""
    fi
}

crearEnv() {
    if [[ -f ".env" ]]; then
        echo ""
        echo "---------------------------Archivo .env ya estaba creado---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Creando .env---------------------------"
        echo ""

        touch .env

        echo ""
        echo "---------------------------Llenando .env---------------------------"
        echo ""

        echo "DB_HOST=localhost" >> .env
        echo "DB_USER=root" >> .env
        echo "DB_PASSWORD=password" >> .env # completar manualmente en .env
        echo "DB_NAME=datos_usuario" >> .env
    fi
}

instalarDotenv() {
    if pip list | grep python-dotenv > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------python-dotenv ya está instalado---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Instalando python-dotenv---------------------------"
        echo ""
        pip install python-dotenv
    fi
}

instalarFlask() {
    if pip list | grep Flask > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Flask ya estaba instalado---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Instalando Flask---------------------------"
        echo ""
        pip install flask
    fi
}

instalarPython312Venv() {
    if apt list --installed | grep python3.12-venv > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Python3.12-venv ya estaba instalado---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Instalando Python3.12-venv---------------------------"
        echo ""
        sudo apt install python3.12-venv
    fi
}

instalarFlaskCors() {
    if pip list | grep flask-cors > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Flask-Cors ya estaba instalado---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Instalando Flask-Cors---------------------------"
        echo ""
        pip install flask-cors
    fi
}

instalarMysqlConnector() {
    if pip list | grep mysql > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Mysql-Connector ya estaba instalado---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Instalando Mysql-Connector---------------------------"
        echo ""
        pip install mysql-connector-python
    fi
}

instalarFlaskSession() {
    if pip list | grep flask_session > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Flask-session ya estaba instalado---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Instalando Flask-session---------------------------"
        echo ""
        pip install flask_session
    fi
}

crearEnv

cd src

instalarPython3
instalarPip3
instalarPython312Venv

crearVenv
ActivacionEntornoVirtual

instalarFlask
instalarFlaskMail
instalarFlaskCors
instalarFlaskSession
instalarMysqlConnector
instalarDotenv
