CREATE DATABASE IF NOT EXISTS datos_usuarios;
USE datos_usuarios;

CREATE TABLE IF NOT EXISTS datos (
    id INT  AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50),
    email_usuario VARCHAR(100),
    contaseña_usuario VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS libros (
    id INT  AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100),
    autor VARCHAR(100),
    codigo_isbn INT (100),
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES datos(id)
);



