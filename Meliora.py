import smtplib
import pymysql
from email.message import EmailMessage
import unicodedata

SMTP_CONFIG = {
    'host': "mail.vargasia.com",
    'port': 587,
    'user': "noreply@vargasia.com",
    'password': "OuTRW9U6f#2yBf6h",
}

conexion = pymysql.connect(
    host='track.vrgs.es',
    user='samuel.villa',
    password='rLh8DbKyu4Y6dwAazJXVN',
    database='kimai',
    
)


CORREOS_USUARIOS = {
    "rafa.vargas": "rafa.vargas@vargasia.com",
    "samuel.villa": "samuel.villa@vargasia.com",
    "admin": "admin@vargasia.com"
}

def limpiar_ascii(texto):
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

def enviar_correo(username, email_destino):
    mensaje = limpiar_ascii(f"⚠️ {username} no imputó nada hoy.")

    msg = EmailMessage()
    msg['Subject'] = "Aviso de imputación"
    msg['From'] = SMTP_CONFIG['user']
    msg['To'] = email_destino
    msg.set_content(mensaje)

    try:
        with smtplib.SMTP(SMTP_CONFIG['host'], SMTP_CONFIG['port'], timeout=10) as smtp:
            smtp.starttls()
            smtp.login(SMTP_CONFIG['user'], SMTP_CONFIG['password'])
            smtp.send_message(msg)
        print(f"Correo enviado a {username}.")
    except:
        # Silenciar errores de envío
        pass

def ha_imputado(cursor, username):
    cursor.execute("""
        SELECT 1
        FROM kimai2_users u
        JOIN kimai2_timesheet t ON u.id = t.user
        WHERE LOWER(u.username) = %s
          AND u.enabled = 1
          AND DATE(t.date_tz) = CURDATE()
          AND TIME(t.start_time) < '12:00:00'
        LIMIT 1
    """, (username,))
    return cursor.fetchone() is not None

def main():
    try:
        conexion = pymysql.connect
        cursor = conexion.cursor()

        cursor.execute("SELECT username FROM kimai2_users WHERE enabled = 1")
        usuarios = [row[0].lower() for row in cursor.fetchall()]

        for username in usuarios:
            if username not in CORREOS_USUARIOS:
                continue

            if not ha_imputado(cursor, username):
                print(f"⚠️ {username} no imputó nada hoy.")
                enviar_correo(username, CORREOS_USUARIOS[username])
            else:
                print(f"✅ {username} sí imputó antes de las 12:00.")

        cursor.close()
        conexion.close()
    except Exception as e:
        print("❌ Error general:", e)

if __name__ == "__main__":
    main()
