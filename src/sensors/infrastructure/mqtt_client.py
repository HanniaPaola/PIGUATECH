# src/sensors/infrastructure/mqtt_client.py
import paho.mqtt.client as mqtt
from src.core.db.connection import SessionLocal
from src.sensors.application.sensor_service import SensorService

MQTT_BROKER_IP = "98.80.91.239"
MQTT_PORT = 1883
MQTT_USERNAME = "tacodorado"
MQTT_PASSWORD = "notecreomai"

TOPICS = {
    "temperature": "sensor.temperatura",
    "water_level": "sensor.agua",
    "turbidity": "sensor.turbidez",
    "weight": "sensor.peso"
}

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    topic = msg.topic

    db = SessionLocal()
    service = SensorService(db)

    if topic == TOPICS["temperature"]:
        service.process_temperature(payload)
    elif topic == TOPICS["water_level"]:
        service.process_water_level(payload)
    elif topic == TOPICS["turbidity"]:
        service.process_turbidity(payload)
    elif topic == TOPICS["weight"]:
        service.process_weight(payload)

    db.close()

def start_mqtt():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_message = on_message

    client.connect(MQTT_BROKER_IP, MQTT_PORT, 60)

    for _, topic in TOPICS.items():
        client.subscribe(topic)
        print(f"📡 Subscribed to {topic}")

    client.loop_start()
