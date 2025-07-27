from flask import Flask, request

app = Flask(__name__)

@app.route('/ping', methods=['POST'])
def ping():
    data = request.get_json()
    print("📥 Datos recibidos:", data)
    return "✅ Conexión exitosa"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
