# src/core/broker/rabbit.py

import os
import pika
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# RabbitMQ Connection

class ConnRabbitMQ:
    def __init__(self):
        self.error = ""
        try:
            rabbitmq_user = os.getenv("RABBITMQ_USER")
            rabbitmq_pass = os.getenv("RABBITMQ_PASS")
            rabbitmq_host = os.getenv("RABBITMQ_HOST")
            rabbitmq_port = os.getenv("RABBITMQ_PORT")

            credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
            parameters = pika.ConnectionParameters(
                host=rabbitmq_host,
                port=int(rabbitmq_port),
                credentials=credentials
            )

            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

        except Exception as e:
            self.error = f"Error connecting to RabbitMQ: {e}"
            self.connection = None
            self.channel = None

    def close(self):
        if self.connection:
            self.connection.close()

# WebSocket Notify

WS_SERVER_HOST = os.getenv("WS_SERVER_HOST", "localhost")
WS_SERVER_PORT = os.getenv("WS_SERVER_PORT", "3000")

WS_SERVER_URL = f"http://{WS_SERVER_HOST}:{WS_SERVER_PORT}/internal/send"

def notify_websocket(receiver: str, content: str):
    payload = {
        "receiver": receiver,
        "payload": json.dumps({
            "sender": "server",
            "receiver": receiver,
            "content": content
        })
    }
    try:
        res = requests.post(WS_SERVER_URL, json=payload)
        res.raise_for_status()
        print(f"✅ Notificación enviada a [{receiver}]: {content}")
    except requests.RequestException as e:
        print(f"❌ Error enviando notificación WS: {e}")
