CREATE DATABASE IF NOT EXISTS datos_usuarios;
USE datos_usuarios;

CREATE TABLE IF NOT EXISTS datos_usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50),
    email_usuario VARCHAR(100),
    contaseña_usuario VARCHAR(100),
    telefono_usuario INT(100),
    direccion_usuario VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,

    titulo VARCHAR(100),
    autor VARCHAR(100),
    editorial VARCHAR(255),
    codigo_isbn INT (100),
    tematica VARCHAR (100),
    
    fecha_publicacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    estado_del_libro ENUM('disponible', 'intercambiado', 'pausa') DEFAULT 'disponible',

    FOREIGN KEY (usuario_id) REFERENCES datos_usuario(id)
);

CREATE TABLE IF NOT EXISTS intercambio_libro(
    codigo_intercambio INT PRIMARY KEY,

    id_libro_publicado INT,
    id_libro_ofrecido INT,

    id_usuario_publicado INT,
    id_usuario_ofrecido INT,
    
    fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_final DATETIME DEFAULT CURRENT_TIMESTAMP,

    estado_del_intercambio ENUM('espera', 'completado', 'cancelado') DEFAULT 'espera'

    FOREIGN KEY (id_libro_publicado) REFERENCES libros(id),
    FOREIGN KEY (id_libro_ofecido) REFERENCES libros(id),
    FOREIGN KEY (id_usuario_publicado) REFERENCES datos_usuario(id),
    FOREIGN KEY (id_usuario_ofrecido) REFERENCES datos_usuario(id)
);



