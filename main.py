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

SLEEP_TIME = 15
SENSOR_IP_ADDRESS = '10.0.5.96'
PORT = 5000

def request_data():
    url = f'http://{SENSOR_IP_ADDRESS}:{PORT}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        log.warning(f'Response from {url}: {response.status_code}')
    return {}

def on_log(client, data, level, buf):
    log.info(f"log: {buf}")


if __name__ == "__main__":
    while True:
        try:
            client = mqtt.Client("astro_sensor", clean_session=False)
            client.connect('mosquitto')
            client.on_log = on_log
            log.info("Pushing data")
            data = request_data()
            log.info(json.dumps(data))
            client.publish("sensors/astro_sensor", json.dumps(data))
            client.disconnect()
        except:
            log.info("Issue with pushing data", exc_info=True)
        time.sleep(SLEEP_TIME)


