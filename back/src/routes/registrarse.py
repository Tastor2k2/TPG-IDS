from ..db import get_connection

def insertar_usuario(nombre: str, mail: str, contrasena: str) -> bool:
    """
    Inserta un nuevo usuario en la tabla 'datos_usuario'.
    PRECONDICIONES
        - String 'nombre', con el nombre del usuario.
        - String 'mail', con el correo electronico del usuario
        - String 'contrasena', con la password del usuario.
    POSTCONDICIONES
        - Si la conexión no es exitosa, se imprime un mensaje informativo y devulve False.
        - Si la conexión es exitosa, se cargan los datos del usuario en la tabla (cursor.execute
          ejecuta el INSERT, conexion.commit confirma la transacción, cursor.close cierra el cursor,
          liberando recursos asociados a la consulta, conexion.close cierra la conexión con la DB y se
          devuelve True).
    """
    conexion = get_connection()

    if conexion is None:
        print("No se pudo obtener conexión a la base de datos")
        return False

    cursor = conexion.cursor()
    sql = """
        INSERT INTO datos_usuario (nombre_usuario, email_usuario, contraseña_usuario)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (nombre, mail, contrasena))
    conexion.commit()
    cursor.close()
    conexion.close()
    return True
