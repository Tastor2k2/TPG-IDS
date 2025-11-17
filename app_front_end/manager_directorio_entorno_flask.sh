#!/bin/bash

crearSubCarpetas() {
    mkdir static
    cd static
    mkdir images
    mkdir css
    cd css
    touch styles.css
    cd ..
    mkdir js
    cd js
    touch script.js
    cd ..
    mkdir fonts
    cd ..
    mkdir templates
    cd templates
    touch index.html
    cd ..
    touch app.py
    echo "---------------------------Carpetas Creadas---------------------------"
    echo ""
}

eliminarDirectorio() {
    source eliminacion_entorno_flask.sh
}

activacionEntornoFlask() {
    source activacion_entorno_flask.sh
}

verificacionSegParametro() {
    if [[ "$1" = "-d" ]]; then
        eliminarDirectorio
        return 0
    elif [[ "$1" = "-a" ]]; then
        activacionEntornoFlask
        return 0
    fi
    main
    return 0
}

main() {
    crearSubCarpetas
    activacionEntornoFlask
}

verificacionSegParametro $1