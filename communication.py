from paho.mqtt.client import Client as MQTTClient
import json

import time
import serial
import re


class Communication(MQTTClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self._serial_id = kwargs["serial_id"]
        self._rfid_port = kwargs["rfid_port"]
        self._baudrate = kwargs["baudrate"]
        self.access_payload = {
            "serial_number": self._serial_id,
            "card_id": "",
            "action": "",
            "msg_type": "access_requested",
        }
        self.config_payload = {
            "serial_number": self._serial_id,
            "msg_type": "configuration",
        }

        self._is_running = True

    def subscribe_config(self, callback):
        topic = f"{self._serial_id}/asset/configuration/onResponded"
        self.subscribe(topic)
        self.message_callback_add(topic, callback)

    def subscribe_access(self, callback):
        topic = f"{self._serial_id}/asset/access/onResponded"
        self.subscribe(topic)
        self.message_callback_add(topic, callback)

    def request_config(self):
        topic = f"asset/configuration/requested"
        return self.publish(topic, json.dumps(self.config_payload))

    def request_access(self, card_id):
        if self.access_payload["card_id"] == card_id:
            if self.access_payload["action"] == "login":
                self.access_payload["action"] = "logout"
            else:
                self.access_payload["action"] = "login"
        else:
            self.access_payload["card_id"] = card_id
            self.access_payload["action"] = "login"
        topic = f"asset/access/requested"
        return self.publish(topic, json.dumps(self.access_payload))

    def valid_card(self):
        try:
            ser = serial.Serial(self._rfid_port, self._baudrate, timeout=1)
            buffer = ""
            rfidPattern = re.compile(b"[\W_]+")
            while self._is_running:
                buffer = buffer + ser.read(ser.inWaiting())
                if "\n" in buffer:
                    lines = buffer.split("\n")
                    last_received = lines[-2]
                    card_id = rfidPattern.sub("", last_received)

                    if card_id:
                        print(card_id)
                        self.request_access(card_id)

                    buffer = ""
                    lines = ""
                time.sleep(1)
        except Exception as e:
            print("Could not read:", e)

    def stop_thread(self):
        self._is_running = False
