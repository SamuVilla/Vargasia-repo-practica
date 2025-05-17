import smtplib
import os 

import smtplib
from email.message import EmailMessage

# Datos de conexión
smtp_host = "mail.vargasia.com" #o cualquier otra dirección
smtp_port = 587  # Podés probar con 465 si usás SSL directo
usuario = "noreply@vargasia.com" #o cualquier otra
contraseña = "OuTRW9U6f#2yBf6h"

# Crear el mensaje
msg = EmailMessage()
msg['Subject'] = "Prueba desde Python"
msg['From'] = usuario
msg['To'] = "samuel.villa@vargasia.com"  # Cambiá esto por el mail real
msg.set_content("Hola! Este es un correo enviado desde un script de Python montado por Samuel Villa en colaboración con ChatGPT y Rafa Vargas. 😊")

# Enviar correo
try:
    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.starttls()  # Seguridad TLS
        smtp.login(usuario, contraseña)
        smtp.send_message(msg)
    print("✅ Correo enviado exitosamente.")
except Exception as e:
    print("❌ Error al enviar el correo:")
    print(e)
