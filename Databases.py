import pymysql

# Conexión
conexion = pymysql.connector.connect(
    host='trck.vgrs.es',
    user='samuel.villa',
    password='rLh8DbKyu4Y6dwAazJXVNq',
    database=''
)

cursor = conexion.cursor()

cursor.execute("SELECT * FROM usuarios")

for fila in cursor.fetchall():
    print(fila)

conexion.close()
