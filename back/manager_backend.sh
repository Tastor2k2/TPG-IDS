#!/bin/bash

# SIN SEGUNDO PARAMETRO: CREA EL ENTORNO CON LA CARPETA NOMBRADA SEGUN EL PRIMER PARAMETRO.
# SEGUNDO PARAMETRO -d: BORRA TODO EL DIRECTORIO DESACTIVANDO PREVIAMENTE EL ENTORNO.
# SEGUNDO PARAMETRO -a: SOLO REALIZA LA ACTIVACION E INSTALACIONES MECESARIAS DENTRO DEL DIRECTORIO.

crearCarpetas() {
    mkdir src
    cd src
    touch app.py
    touch db.py
    touch init_db.py
    touch init_db.sql
    mkdir routes
    cd routes
    touch carga_libros.py
    touch datos_usuarios.py
    touch intercambio_libros.py
    cd ..
    cd ..
    echo "---------------------------Carpetas Creadas---------------------------"
    echo ""
}

eliminarBack() {
    source eliminacion_backend.sh
}

activarBack() {
    source activacion_backend.sh
}

verificacionParametro() {
    if [[ "$1" = "-d" ]]; then
        eliminarBack
        return 0
    elif [[ "$1" = "-a" ]]; then
        activarBack
        return 0
    fi
    main
    return 0
}

main() {
    crearCarpetas
    activarBack
}

verificacionParametro $1