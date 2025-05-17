import smtplib
import os 
import pymysql # type: ignore
import smtplib
from email.message import EmailMessage



# Datos de conexión
smtp_host = "mail.vargasia.com"
smtp_port = 587  # Podés probar con 465 si usás SSL directo
usuario = "noreply@vargasia.com"
contraseña = "OuTRW9U6f#2yBf6h"

# Crear el mensaje
msg = EmailMessage()
msg['Subject'] = "Prueba desde Python"
msg['From'] = usuario
msg['To'] = "samuel.villa@vargasia.com"  # Cambiá esto por el mail real
msg.set_content("Hola! Este es un correo enviado desde un script de Python montado por Samuel Villa en colaboración con ChatGPT y Rafa Vargas. 😊")

import pymysql
import smtplib
from email.message import EmailMessage
from datetime import datetime, time

# Configuración de base de datos
db_config = {
    'host': 'track.vrgs.es',
    'user': 'samuel.villa',
    'password': 'rLh8DbKyu4Y6dwAazJXVNq',
    'database': 'kimai'
}

# Configuración del correo
EMAIL_ORIGEN = 'tu_email@dominio.com'
EMAIL_PASSWORD = 'tu_contraseña'
SMTP_SERVER = 'smtp.dominio.com'
SMTP_PORT = 587

# Usuarios y correos
usuarios = {
    'admin': 'admin@empresa.com',
    'beatriz.villanueva': 'beatriz@empresa.com',
    'rafa.vargas': 'rafa@empresa.com',
    'samuel.villa': 'samuel@empresa.com'
}

# Enviar correo de aviso
def enviar_aviso(usuario, correo, hora=None):
    hora_texto = f"a las {hora}" if hora else "ninguna tarea registrada"
    msg = EmailMessage()
    msg['Subject'] = f'[AVISO] {usuario}: imputación tardía o ausente'
    msg['From'] = EMAIL_ORIGEN
    msg['To'] = correo
    msg.set_content(
        f'Hola {usuario},\n\nNo se ha registrado una imputación válida antes de las 12:00 de hoy.\n'
        f'Se detectó: {hora_texto}.\n\nPor favor, regulariza tu jornada.\n\nGracias.'
    )
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ORIGEN, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f'📧 Enviado aviso a {usuario}')
    except Exception as e:
        print(f'❌ Error al enviar email a {usuario}: {e}')

# Consulta y verificación
try:
    conexion = pymysql.connect(**db_config)
    cursor = conexion.cursor()

    for username, email in usuarios.items():
        sql = """
        SELECT MIN(t.start_time)
        FROM kimai2_users u
        JOIN kimai2_timesheet t ON u.id = t.user
        WHERE LOWER(CONCAT(SUBSTRING_INDEX(u.username, ' ', 1), '.', SUBSTRING_INDEX(u.username, ' ', -1))) = %s
          AND t.date_tz = CURDATE();
        """
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        primera_tarea = result[0]

        if primera_tarea:
            hora = primera_tarea.time()
            if hora < time(12, 0):
                print(f'✅ {username} imputó a las {hora}')
            else:
                print(f'⚠️ {username} imputó tarde: {hora}')
                enviar_aviso(username, email, hora)
        else:
            print(f'⚠️ {username} no imputó nada hoy')
            enviar_aviso(username, email)

except Exception as e:
    print(f'❌ Error de base de datos: {e}')

finally:
    if 'conexion' in locals():
        conexion.close()