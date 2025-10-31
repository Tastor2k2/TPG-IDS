#!/bin/bash

mkdir front
cd front
mkdir templates
mkdir .venv
mkdir static
cd static
mkdir css
mkdir js
mkdir images
cd ..
touch app.py

pipenv install flask
pipenv shell

export FLASK_APP=app.py
export FLASK_DEBUG=1

flask run

