import smtplib
from email.message import EmailMessage
import mysql.connector # type: ignore

# Configuración del correo
smtp_host = "mail.vargasia.com"
smtp_port = 587
usuario = "noreply@vargasia.com"
contraseña = "OuTRW9U6f#2yBf6h"
destinatario = "samuel.villa@vargasia.com"

try:
    # Conexión a la base de datos MySQL
    conexion = mysql.connector.connect(
        host='track.vrgs.es',          # Cambia si es otro host
        user='samuel.villa',         # Cambia por tu usuario de base de datos
        password='rLh8DbKyu4Y6dwAazJXVNq',       # Cambia por tu contraseña
        database='kimai'       # Cambia por tu base de datos
    )
    cursor = conexion.cursor()

    # Consulta para detectar inconsistencias entre duration y tiempo real
    cursor.execute("""
        SELECT id, user, start_time, end_time, duration
        FROM kimai2_timesheet
        WHERE end_time IS NOT NULL
          AND duration IS NOT NULL
          AND duration != TIMESTAMPDIFF(SECOND, start_time, end_time)
    """)

    resultados = cursor.fetchall()

    if resultados:
        # Crear el mensaje
        msg = EmailMessage()
        msg['Subject'] = "Prueba desde Python - Inconsistencias detectadas"
        msg['From'] = "noreply@vargasia.com"
        msg['To'] = "samuel.villa@vargasia.com"


        cuerpo = (
            "Hola! Este es un correo enviado desde un script de Python montado por Samuel Villa "
            "en colaboración con ChatGPT y Rafa Vargas. 😊\n\n"
            "Se detectaron registros con diferencias entre 'duration' y el tiempo real trabajado:\n\n"
        )

        for fila in resultados:
            cuerpo += (
                f"ID: {fila[0]} | Usuario: {fila[1]} | Inicio: {fila[2]} | Fin: {fila[3]} | "
                f"Duration registrado: {fila[4]} seg\n"
            )

        cuerpo += "\nFavor revisar. Descansar también es importante. 😉"

        msg.set_content(cuerpo)

        # Enviar el correo
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(usuario, contraseña)
            smtp.send_message(msg)

        print("✅ Correo enviado exitosamente por inconsistencias.")
    else:
        print("✅ No se detectaron inconsistencias. No se envía correo.")

except Exception as e:
    print("❌ Error al procesar:")
    print(e)

finally:
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
