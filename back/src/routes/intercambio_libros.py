from flask import Blueprint, jsonify, request
from src.db import get_connection

intercambio_libros_bp  = Blueprint("intercambio_libros", __name__)

@intercambio_libros_bp.route('/solicitar_intercambio', methods=['POST'])
def solicitar_intercambio():
    data = request.get_json()
    libro_solicitado = data.get('libro_solicitado')
    solicitante_id = data.get('solicitante_id')

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
