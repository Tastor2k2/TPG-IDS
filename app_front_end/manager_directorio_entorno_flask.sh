#!/bin/bash

# SIN SEGUNDO PARAMETRO: CREA EL ENTORNO CON LA CARPETA NOMBRADA SEGUN EL PRIMER PARAMETRO.
# SEGUNDO PARAMETRO -d: BORRA TODO EL DIRECTORIO DESACTIVANDO PREVIAMENTE EL ENTORNO.
# SEGUNDO PARAMETRO -a: SOLO REALIZA LA ACTIVACION E INSTALACION DE FLASK DENTRO DEL DIRECTORIO.

# Ejecutar Para Crear (y quedar dentro del directorio):
# source manager_directorio_entorno_flask.sh nombre_archivo

# Ejecutar Para Crear (y quedar fuera del directorio):
# bash manager_directorio_entorno_flask.sh nombre_archivo

# Ejecutar para borrar todo el directorio:
# source manager_directorio_entorno_flask.sh nombre_archivo -d

# Ejecutar para activar directorio:
# source manager_directorio_entorno_flask.sh nombre_archivo -a

# PROJECT_FOLDER_NAME=$1

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

# eliminarDirectorio() {
#     source eliminacion_entorno_flask.sh $PROJECT_FOLDER_NAME
#     rm -r "$PROJECT_FOLDER_NAME"
# }

eliminarDirectorio() {
    source eliminacion_entorno_flask.sh
}

# activacionEntornoFlask() {
#     source activacion_entorno_flask.sh $PROJECT_FOLDER_NAME
# }

activacionEntornoFlask() {
    source activacion_entorno_flask.sh
}

# verificacionSegParametro() {
#     if [[ -d "$PROJECT_FOLDER_NAME" ]]; then
#         if [[ "$2" = "-d" ]]; then
#             eliminarDirectorio $PROJECT_FOLDER_NAME
#             return 0
#         elif [[ "$2" = "-a" ]]; then
#             activacionEntornoFlask $PROJECT_FOLDER_NAME
#             return 0
#         fi
#     else
#         main $PROJECT_FOLDER_NAME
#         return 0
#     fi
# }

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

# crearCarpetaDirectorio() {
#     if [ -d "$PROJECT_FOLDER_NAME" ]; then
#     echo ""
#     echo "---------------------------La carpeta '$PROJECT_FOLDER_NAME' ya existe.---------------------------"
#     echo ""
#     else
#         mkdir "$PROJECT_FOLDER_NAME"
#         echo ""
#         echo "------------------------Carpeta '$PROJECT_FOLDER_NAME' creada.------------------------"
#         echo ""
#     fi
# }

main() {
    # crearCarpetaDirectorio $PROJECT_FOLDER_NAME
    # cd "$PROJECT_FOLDER_NAME"
    crearSubCarpetas
    # cd ..
    # activacionEntornoFlask $PROJECT_FOLDER_NAME
    activacionEntornoFlask
}

# verificacionSegParametro $PROJECT_FOLDER_NAME $2

verificacionSegParametro $1

# En vs code, dentro del entorno en app.py tocar F1 y colocar
# >interpreter, luego Enter y elegir python (.venv)