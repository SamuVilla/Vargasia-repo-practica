  import sqlite3

# Conectar o crear la base de datos
conexion = sqlite3.connect('mi_base_de_datos.db')

# Crear cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# Crear una tabla de ejemplo
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        edad INTEGER
    )
''')

# Guardar cambios y cerrar conexión
conexion.commit()
conexion.close()


import mysql.connector

# Conexión
conexion = mysql.connector.connect(
    host='localhost',
    user='tu_usuario',
    password='tu_contraseña',
    database='nombre_base_datos'
)

cursor = conexion.cursor()

cursor.execute("SELECT * FROM usuarios")

for fila in cursor.fetchall():
    print(fila)

conexion.close()


import psycopg2

conexion = psycopg2.connect(
    host='localhost',
    database='nombre_base_datos',
    user='tu_usuario',
    password='tu_contraseña'
)

cursor = conexion.cursor()

cursor.execute("SELECT * FROM usuarios")

for fila in cursor.fetchall():
    print(fila)

conexion.close()
