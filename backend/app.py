from flask import Flask, jsonify
import threading
import json
import paho.mqtt.client as mqtt

app = Flask(_name_)

# --------------------------
# Variabel penyimpanan data
# --------------------------
latest_data = {
    "moisturePercent": 0,
    "soilTemperature": 0,
    "suhuUdara": 0,
    "kelembapanUdara": 0,
    "mode": "AUTO",
    "pumpState": "MATI"
}

# --------------------------
# MQTT CONFIG
# --------------------------
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "irigasi/sensor"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("MQTT Connected:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global latest_data
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        latest_data = data
        print("Data diterima:", latest_data)
    except Exception as e:
        print("Error decode:", e)

client.on_connect = on_connect
client.on_message = on_message

# Jalankan MQTT Loop pada thread terpisah
def mqtt_thread():
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

threading.Thread(target=mqtt_thread, daemon=True).start()

# --------------------------
# API ENDPOINT
# --------------------------
@app.get("/sensor")
def get_sensor():
    return jsonify(latest_data)

# >>> ENDPOINT UNTUK FRONTEND <<<
@app.get("/get_data")
def get_data():
    return jsonify(latest_data)

@app.get("/")
def home():
    return "MQTT Flask Backend Running"

# --------------------------
# RUN FLASK
# --------------------------
if _name_ == "_main_":
    app.run(host="0.0.0.0", port=8000)
