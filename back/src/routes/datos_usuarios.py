from flask import Blueprint, jsonify, request
from src.db import get_connection

datos_usuarios  = Blueprint("datos", __name__)