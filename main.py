import time
import logging

import requests
import json
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO)
logFormatter = logging.Formatter(
    "%(asctime)s %(module)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
)
log = logging.getLogger()

def get_data():
    ip_address = '10.0.5.96'
    port = 5000
    url = f'http://{ip_address}:{port}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

def on_log(client, data, level, buf):
    log.info(f"log: {buf}")


def parse_data():
    mqtt_broker_address = "10.0.5.50"
    while True:
        try:
            client = mqtt.Client("astro_sensor", clean_session=False)
            client.connect(mqtt_broker_address)
            client.on_log = on_log
            log.info("Pushing data")
            data = get_data()
            log.info(json.dumps(data))
            client.publish("sensors/astro_sensor", json.dumps(data))
            client.disconnect()
            time.sleep(15)
        except:
            log.info("Issue with pushing data", exc_info=True)
            time.sleep(15)


if __name__ == "__main__":
    parse_data()
