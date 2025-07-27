from flask import Flask, request, render_template
import mysql.connector
from db_config import db_config
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM mediciones ORDER BY fecha DESC LIMIT 10")
        datos = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', datos=datos)
    except Exception as e:
        return f"❌ Error al obtener datos: {e}", 500

@app.route('/datos', methods=['POST'])
def recibir_datos():
    datos = request.get_json()
    print("📥 Datos recibidos:", datos)
    temp = datos.get('temperatura')
    hum = datos.get('humedad')
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mediciones (temperatura, humedad, fecha) VALUES (%s, %s, %s)",
            (temp, hum, fecha)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return '✅ Datos guardados correctamente'
    except Exception as e:
        print("❌ Error al guardar:", e)
        return f'Error: {e}', 500
# ... tus rutas van arriba

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
