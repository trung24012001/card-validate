import sys
import configparser
import uuid
import json
import threading

from PyQt5.QtWidgets import QApplication
from communication import Communication
from ui import UI

config = configparser.ConfigParser()
config.read("config.ini")
config_default = config["DEFAULT"]
config_info = config["INFO"]

baudrate = config_default["BAUDRATE"]
rfid_port = config_default["RFID_PORT"]
serial_id = config_default["SERIAL"]
mqtt_client_id = f"python-mqtt-{uuid.uuid4()}"
mqtt_host = config_default["MQTT_HOST"]
mqtt_port = int(config_default["MQTT_PORT"])
web_host = config_default["WEB_HOST"]
web_port = int(config_default["WEB_PORT"])

phone_number = config_info["PHONE"]


def main():

    app = QApplication(sys.argv)
    ui = UI(phone_number=phone_number)
    comm = Communication(
        mqtt_client_id, serial_id=serial_id, rfid_port=rfid_port, baudrate=baudrate
    )

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_log(client, userdata, level, buf):
        print(f"log: {buf}")

    def on_access(client, userdata, msg):
        print("access:", msg.payload)
        ui.access_signal.emit(json.dumps(json.loads(msg.payload)))

    def on_config(client, userdata, msg):
        print("config", msg.payload)
        ui.config_signal.emit(json.dumps(json.loads(msg.payload)))

    comm.connect(mqtt_host, mqtt_port)
    comm.on_connect = on_connect
    comm.on_log = on_log
    comm.subscribe_config(on_config)
    comm.subscribe_access(on_access)
    comm.request_config()
    comm.loop_start()
    thread = threading.Thread(target=comm.valid_card)
    thread.start()

    ui.show()
    if app.exec() == 0:
        comm.stop_thread()
        sys.exit(0)


if __name__ == "__main__":
    main()
