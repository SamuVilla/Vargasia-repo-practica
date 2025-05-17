import smtplib
import pymysql  # type: ignore
from email.message import EmailMessage
import unicodedata
sql = """
SELECT u.id, u.username, SUM(TIMESTAMPDIFF(SECOND, t.start_time, t.end_time) / 3600) AS horas_imputadas
FROM kimai2_users u
JOIN kimai2_timesheet t ON u.id = t.user
WHERE u.enabled = 1
AND DATE(t.date_tz) = CURDATE()  -- Solo actividades de hoy
GROUP BY u.id, u.username
HAVING horas_imputadas > 12;
"""



# Configuración
SMTP_CONFIG = {
    "host": "mail.vargasia.com",
    "port": 587,
    "user": "noreply@vargasia.com",
    "password": "OuTRW9U6f#2yBf6h",
}

DB_CONFIG = {
    'host': 'track.vrgs.es',
    'user': 'samuel.villa',
    'password': 'rLh8DbKyu4Y6dwAazJXVN',
    'database': 'kimai',
    'charset': 'utf8mb4',
}

CORREOS_USUARIOS = {
   
    "rafa.vargas": "rafa.vargas@vargasia.com",
    "samuel.villa": "samuel.villa@vargasia.com",
    "admin": "admin@vargasia.com"
}