import os
import re
import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- Configuración del correo electrónico ---
email_from = "tucorreoaqui@gmail.com"
email_to = "destino@cualquiera.com"
app_password = "xxxx mpvd qadf aost"
smtp_server = "smtp.gmail.com"
smtp_port = 587

# --- Script de auditoría ---
# La ruta del archivo de log original, sin copiarlo.
log_file_path = r"C:\Windows\system32\LogFiles\Firewall\pfirewall.log"

bloqueos = []
try:
    with open(log_file_path, "r", encoding="utf-8") as f:
        for line in f:
            if "DROP" in line:
                bloqueos.append(line)
except FileNotFoundError:
    print("Error: No se pudo encontrar el archivo de registro del firewall.")
    exit()
except PermissionError:
    print("Error: Permiso denegado. Asegúrate de ejecutar el script como administrador.")
    exit()

if bloqueos:
    print("Se encontraron eventos de bloqueo de firewall. Preparando alerta...")
    cuerpo_correo = "Se detectaron los siguientes eventos de bloqueo en tu firewall:\n\n"

    for line in bloqueos:
        # Usa una expresión regular para encontrar la fecha, IP y puerto
        match = re.search(r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).*? DROP.*? (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?DPT=(\d+)", line)
        
        if match:
            fecha_bloqueo = "-".join(match.groups()[0:6])
            ip = match.group(7)
            puerto = match.group(8)

            # Obtiene la geolocalización de la IP
            try:
                geo_info = requests.get(f"http://ip-api.com/json/{ip}").json()
                pais = geo_info.get("country", "Desconocido")
                ciudad = geo_info.get("city", "Desconocida")
            except requests.exceptions.RequestException:
                pais = "Desconocido"
                ciudad = "Desconocida"

            # Agrega los detalles al cuerpo del correo
            cuerpo_correo += f"• Fecha y Hora: {fecha_bloqueo}\n"
            cuerpo_correo += f"• IP de Origen: {ip}\n"
            cuerpo_correo += f"• Puerto de Destino: {puerto}\n"
            cuerpo_correo += f"• Geolocalización: {ciudad}, {pais}\n"
            cuerpo_correo += "----------------------------------------------\n"

    cuerpo_correo += "\nPara una revisión más detallada, se adjunta el archivo de registro completo."

    # Prepara el correo electrónico
    msg = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = "Alerta de Seguridad - Intento de Conexión No Autorizado"

    msg.attach(MIMEText(cuerpo_correo, "plain"))

    # Adjunta el archivo de log (directamente desde la ruta original)
    try:
        with open(log_file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(log_file_path)}")
        msg.attach(part)
    except PermissionError:
        print("Advertencia: No se pudo adjuntar el archivo de log por falta de permisos.")

    # Envía el correo
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(email_from, app_password)
            server.sendmail(email_from, email_to, msg.as_string())
        print("¡Alerta enviada correctamente!")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

else:
    print("No se encontraron eventos de bloqueo de firewall en el período seleccionado.")
