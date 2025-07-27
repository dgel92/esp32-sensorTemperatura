import mysql.connector
from mysql.connector import Error

# ⚠️ Reemplazá estos datos con los de tu panel de Clever Cloud
db_config = {
    'host': 'btkgeq5na6vml0occnfc-mysql.services.clever-cloud.com',
    'user': 'uft0hfx1ip7dmize',
    'password': 'Sdejr1KMIFmRPOgNDm7n',
    'database': 'btkgeq5na6vml0occnfc',
    'port': 3306
}

try:
    print("Conectando a la base de datos...")
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        print("✅ Conexión exitosa.")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM mediciones ORDER BY fecha DESC LIMIT 5")
        rows = cursor.fetchall()
        print("\nÚltimos 5 registros:")
        for row in rows:
            print(row)
    else:
        print("❌ No se pudo conectar.")

except Error as e:
    print("❌ Error al conectar a la base de datos:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("🔌 Conexión cerrada.")
