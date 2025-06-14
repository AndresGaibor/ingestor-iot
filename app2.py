import os
import time
from dotenv import load_dotenv

import psycopg2
import paho.mqtt.client as mqtt

# Carga variables de entorno desde .env
load_dotenv()

# Parámetros de conexión a PostgreSQL
params = {
    "host":     os.getenv("DB_HOST", "db"),
    "dbname":   os.getenv("DB_NAME"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
}

# 1) Esperar a que la base de datos esté lista
while True:
    try:
        DB = psycopg2.connect(**params)
        print("✅ Conectado a PostgreSQL")
        break
    except psycopg2.OperationalError:
        print("→ DB no lista. Reintentando en 2s…")
        time.sleep(2)

cur = DB.cursor()

# 2) Crear extensión y tabla si no existen
cur.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")
cur.execute("""
    CREATE TABLE IF NOT EXISTS measurements(
        time TIMESTAMPTZ DEFAULT now(),
        topic TEXT,
        value DOUBLE PRECISION
    );
""")
DB.commit()

# 3) Inserción de prueba inicial
cur.execute("""
    INSERT INTO measurements(topic, value)
    VALUES ('sensors/temperature', 0.0);
""")
DB.commit()

# 4) Callback para manejar mensajes MQTT
def on_message(client, userdata, msg):
    try:
        val = float(msg.payload.decode())
        cur.execute(
            "INSERT INTO measurements(topic, value) VALUES (%s, %s)",
            (msg.topic, val)
        )
        DB.commit()
        print("OK:", msg.topic, val)
    except Exception as e:
        print("Error al procesar mensaje:", e)

# 5) Configurar y arrancar cliente MQTT
client = mqtt.Client()
# client.tls_set(ca_certs="/certs/ca.crt")
client.on_message = on_message

broker = os.getenv("MQTT_BROKER", "mqtt-broker")
port   = int(os.getenv("MQTT_PORT", 1883))
topic  = os.getenv("MQTT_TOPIC", "sensors/temperature")

print(f"Conectando a {broker}:{port} → {topic}")
client.connect(broker, port)
client.subscribe(topic)

# 6) Bucle principal que mantiene el contenedor vivo
client.loop_forever()