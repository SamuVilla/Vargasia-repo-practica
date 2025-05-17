import pymysql  # type: ignore

# Conexión
conexion = pymysql.connect(
    host='track.vrgs.es',
    user='samuel.villa',
    password='rLh8DbKyu4Y6dwAazJXVNq',
    database='kimai'
)

cursor = conexion.cursor()

# Consulta con JOIN
sql = """
SELECT u.username, t.begin, t.end, t.duration
FROM kimai2_users u
JOIN kimai2_timesheet t ON u.id = t.user
LIMIT 10
"""

cursor.execute(sql)

for fila in cursor.fetchall():
    print(fila)

conexion.close()
