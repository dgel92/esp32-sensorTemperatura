from flask import Flask, request
import mysql.connector

app = Flask(__name__)

# Datos de tu base de datos en Clever Cloud
db_config = {
    'host': 'TU_HOST',
    'user': 'TU_USUARIO',
    'password': 'TU_CONTRASEÑA',
    'database': 'TU_BASE',
    'port': 3306
}

@app.route('/guardar', methods=['POST'])
def guardar():
    data = request.json
    temp = data.get('temp')
    hum = data.get('hum')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO datos (temperatura, humedad) VALUES (%s, %s)", (temp, hum))
        conn.commit()
        cursor.close()
        conn.close()
        return 'OK', 200
    except Exception as e:
        return f'Error: {e}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
