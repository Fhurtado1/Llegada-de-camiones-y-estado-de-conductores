from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import smtplib
import os
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)  # Esta línea habilita CORS en toda la aplicación

# Configura los detalles de correo electrónico
EMAIL_FROM = os.getenv('EMAIL_FROM')
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAIL_TO = os.getenv('EMAIL_TO')

@app.route('/ping', methods=['GET'])
def ping():
    return "pong"

# Función para enviar notificación por correo
def enviar_notificacion_salida(email_destinatario, nombre_conductor):
    try:
        mensaje = MIMEText(f"El conductor {nombre_conductor} ha salido del predio logístico.")
        mensaje['Subject'] = 'Salida del Predio Logístico'
        mensaje['From'] = EMAIL_FROM
        mensaje['To'] = email_destinatario

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(mensaje['From'], [mensaje['To']], mensaje.as_string())
        print("Notificación de salida enviada correctamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Ruta para obtener la lista de conductores y sus ubicaciones
@app.route('/conductores', methods=['GET'])
def obtener_conductores():
    try:
        conn = sqlite3.connect('predio_logistico.db')
        c = conn.cursor()
        c.execute('''
            SELECT conductores.id, conductores.nombre, conductores.dni, conductores.placa, 
                   ubicaciones.ubicacion, ubicaciones.hora_entrada, ubicaciones.hora_salida
            FROM conductores
            LEFT JOIN ubicaciones ON conductores.id = ubicaciones.id_conductor
            WHERE ubicaciones.hora_salida IS NULL
        ''')
        conductores = c.fetchall()
        conn.close()

        # Estructura los datos en un formato JSON adecuado
        conductores_json = [
            {
                "id": conductor[0],
                "nombre": conductor[1],
                "dni": conductor[2],
                "placa": conductor[3],
                "ubicacion": conductor[4],
                "hora_entrada": conductor[5],
                "hora_salida": conductor[6]
            }
            for conductor in conductores
        ]
        return jsonify(conductores_json)
    except Exception as e:
        print(f"Error al obtener conductores: {e}")
        return jsonify({"error": "Error al obtener conductores"}), 500

# Ruta para registrar la llegada y asignar ubicación
@app.route('/conductores/<int:id>/ubicacion', methods=['POST'])
def actualizar_ubicacion(id):
    data = request.json
    ubicacion = data.get('ubicacion')
    if ubicacion not in ['vigilancia', 'playa de espera', 'dock 1', 'dock 2', 'dock 3', 'dock 4', 'dock 5', 'salida']:
        return jsonify({"error": "Ubicación inválida"}), 400
    
    try:
        conn = sqlite3.connect('predio_logistico.db')
        c = conn.cursor()
        c.execute("INSERT INTO ubicaciones (id_conductor, ubicacion) VALUES (?, ?)", (id, ubicacion))
        conn.commit()
        conn.close()
        return jsonify({"message": "Ubicación actualizada"}), 200
    except Exception as e:
        print(f"Error al actualizar ubicación: {e}")
        return jsonify({"error": "Error al actualizar ubicación"}), 500

# Ruta para registrar la salida de un conductor
@app.route('/conductores/<int:id>/salida', methods=['POST'])
def registrar_salida(id):
    try:
        conn = sqlite3.connect('predio_logistico.db')
        c = conn.cursor()
        c.execute("UPDATE ubicaciones SET hora_salida = CURRENT_TIMESTAMP WHERE id_conductor = ? AND hora_salida IS NULL", (id,))
        conn.commit()

        # Obtener información del conductor
        c.execute("SELECT nombre FROM conductores WHERE id = ?", (id,))
        conductor = c.fetchone()
        conn.close()

        if conductor:
            # Enviar notificación de salida
            enviar_notificacion_salida(EMAIL_TO, conductor[0])
            return jsonify({"message": "Salida registrada y notificación enviada"}), 200
        else:
            return jsonify({"error": "Conductor no encontrado"}), 404
    except Exception as e:
        print(f"Error al registrar salida: {e}")
        return jsonify({"error": "Error al registrar salida"}), 500

if __name__ == '__main__':
    app.run(debug=True)

