#!/bin/bash

instalarPython3() {
    if python3 --version > /dev/null 2>&1 ; then
    echo ""
    echo "---------------------------Python3 ya esta instalado---------------------------"
    echo ""
    else
        echo ""
        echo "---------------------------Python3 se instalará---------------------------"
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
        echo "---------------------------Pip3 se instalará---------------------------"
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
        echo "---------------------------Flask-Mail se instalará---------------------------"
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
        echo "SECRET_KEY=una-clave-secreta-muy-larga-y-unica" >> .env
        echo "MAIL_SERVER=smtp.gmail.com" >> .env
        echo "MAIL_PORT=587" >> .env
        echo "MAIL_USE_TLS=True" >> .env
        echo "MAIL_USE_SSL=False" >> .env
        echo "MAIL_USERNAME=tu-email@gmail.com" >> .env
        echo "MAIL_PASSWORD=tu-app-password" >> .env
        echo "MAIL_DEFAULT_SENDER=tu-email@gmail.com" >> .env
    fi
}

instalarDotenv() {
    if pip list | grep python-dotenv > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------python-dotenv ya está instalado---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------python-dotenv se instalará---------------------------"
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

instalarRequests() {
    if pip list | grep requests > /dev/null 2>&1 ; then
        echo ""
        echo "---------------------------Requests ya estaba instalado---------------------------"
        echo ""
    else
        echo ""
        echo "---------------------------Instalando Requests---------------------------"
        echo ""
        pip install requests
    fi
}

ejecutar() {
    echo ""
    echo "---------------------------Ejecutando el entorno---------------------------"
    echo ""
    python3 app.py
}

instalarPython3

instalarPip3

instalarPython312Venv

crearVenv

crearEnv

ActivacionEntornoVirtual

instalarFlask

instalarFlaskMail

instalarDotenv

instalarMysqlConnector

instalarRequests

ejecutar