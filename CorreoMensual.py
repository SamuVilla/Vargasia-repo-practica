import smtplib
from email.message import EmailMessage
import mysql.connector
from datetime import datetime

# Configuración del correo
smtp_host = "mail.vargasia.com"
smtp_port = 587
usuario = "noreply@vargasia.com"
contraseña = "OuTRW9U6f#2yBf6h"
destinatario = "samuel.villa@vargasia.com"

# Umbral de alerta (90%)
ALERTA_UMBRAL = 0.9

try:
    # Conexión a la base de datos
    conexion = mysql.connector.connect(
        host='track.vrgs.es',          # Cambia si es otro host
        user='samuel.villa',         # Cambia por tu usuario de base de datos
        password='rLh8DbKyu4Y6dwAazJXVNq',       # Cambia por tu contraseña
        database='kimai'       # Cambia por tu base de datos
    )
    cursor = conexion.cursor(dictionary=True)

    # Consulta de proyectos visibles con presupuesto de tiempo (> 0)
    cursor.execute("""
        SELECT p.id, p.name, p.time_budget, p.budget_type
        FROM kimai2_projects p
        WHERE p.visible = 1 AND p.time_budget IS NOT NULL AND p.time_budget > 0
    """)
    proyectos = cursor.fetchall()

    alertas = []

    for proyecto in proyectos:
        pid = proyecto['id']
        nombre = proyecto['name']
        presupuesto_horas = float(proyecto['time_budget'])
        tipo = proyecto['budget_type'] or 'lifetime'

        # Consulta de horas trabajadas (en segundos)
        if tipo == 'monthly':
            cursor.execute("""
                SELECT SUM(duration) AS total_segundos
                FROM kimai2_timesheet
                WHERE project_id = %s
                AND billable = 1
                AND start_time >= DATE_FORMAT(NOW(), '%%Y-%%m-01')
                AND start_time < DATE_ADD(DATE_FORMAT(NOW(), '%%Y-%%m-01'), INTERVAL 1 MONTH)
            """, (pid,))
        else:
            cursor.execute("""
                SELECT SUM(duration) AS total_segundos
                FROM kimai2_timesheet
                WHERE project_id = %s
                AND billable = 1
            """, (pid,))

        resultado = cursor.fetchone()
        total_segundos = resultado['total_segundos'] or 0
        horas_trabajadas = total_segundos / 3600

        # Comparación con el presupuesto
        if horas_trabajadas >= presupuesto_horas * ALERTA_UMBRAL:
            porcentaje = (horas_trabajadas / presupuesto_horas) * 100
            tipo_texto = "mensual" if tipo == 'monthly' else "total"
            alertas.append(
                f"🔔 Proyecto: {nombre}\n"
                f"Tipo de presupuesto: {tipo_texto}\n"
                f"Horas trabajadas: {horas_trabajadas:.2f}h / {presupuesto_horas:.2f}h "
                f"({porcentaje:.1f}%)\n"
            )

    # Enviar correo si hay alertas
    if alertas:
        msg = EmailMessage()
        msg['Subject'] = "⚠️ Alerta de presupuesto de horas en proyectos Kimai"
        msg['From'] = usuario
        msg['To'] = destinatario
        msg.set_content(
            "Se detectaron proyectos que han superado el 90% de su presupuesto de horas:\n\n"
            + "\n".join(alertas)
        )

        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(usuario, contraseña)
            smtp.send_message(msg)

        print("📧 Correo enviado con alertas de presupuesto.")
    else:
        print("✅ Todos los proyectos están dentro del presupuesto.")

except Exception as e:
    print("❌ Error al procesar:")
    print(e)

finally:
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
