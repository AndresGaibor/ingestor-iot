import os
from dotenv import load_dotenv

load_dotenv()  # carga variables desde .env

import json, ssl, psycopg2, paho.mqtt.client as mqtt
DB = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)
cur = DB.cursor()
cur.execute("""CREATE EXTENSION IF NOT EXISTS timescaledb;""")
cur.execute("""
CREATE TABLE IF NOT EXISTS measurements(
time TIMESTAMPTZ DEFAULT now(),
topic TEXT, value DOUBLE PRECISION);
"""); DB.commit()

cur.execute("""
INSERT INTO measurements(topic,value)
VALUES ('sensors/temperature', 0.0);
"""); DB.commit()

def on_msg(c,u,m):
	val = float(m.payload.decode())
	cur.execute("INSERT INTO measurements(topic,value) VALUES (%s,%s)",
	(m.topic,val)); DB.commit()
	print("OK:", m.topic, val)
	client = mqtt.Client()
	client.tls_set(ca_certs="/certs/ca.crt")
	client.on_message = on_msg
	client.connect(
      os.getenv("MQTT_BROKER"),
      int(os.getenv("MQTT_PORT"))
    )
	client.subscribe(os.getenv("MQTT_TOPIC"))
	client.loop_forever()